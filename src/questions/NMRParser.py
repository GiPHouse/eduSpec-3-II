import re
from typing import Any, Optional, cast

import numpy as np


def convertASDF(XYYdata: str) -> np.ndarray:
    """Converts string of ASDF data to an array of floats.

    Parameters
    ----------
    XYYdata: string
        encoded string which, once decoded, starts with an X value followed by 1 or more Y data points
        In case of DIF(DUP) data, the first Y data point is expected to represent a checkpoint.
        Supported are AFFN, PAC, SQZ, DIF, DUP and DIFDUP encodings

    Returns
    -------
    ndarray
        1-D array with the extracted Y values
    """
    SQZ = {
        "@": "0",
        "A": "1",
        "B": "2",
        "C": "3",
        "D": "4",
        "E": "5",
        "F": "6",
        "G": "7",
        "H": "8",
        "I": "9",
        "a": "-1",
        "b": "-2",
        "c": "-3",
        "d": "-4",
        "e": "-5",
        "f": "-6",
        "g": "-7",
        "h": "-8",
        "i": "-9",
    }
    DIF = {
        "%": "0",
        "J": "1",
        "K": "2",
        "L": "3",
        "M": "4",
        "N": "5",
        "O": "6",
        "P": "7",
        "Q": "8",
        "R": "9",
        "j": "-1",
        "k": "-2",
        "l": "-3",
        "m": "-4",
        "n": "-5",
        "o": "-6",
        "p": "-7",
        "q": "-8",
        "r": "-9",
    }
    DUP = {"S": "1", "T": "2", "U": "3", "V": "4", "W": "5", "X": "6", "Y": "7", "Z": "8", "s": "9"}

    numberSpacerCharacters = ("+", " ", ",")

    def processNumber(val: str, previousOperation: Optional[str]) -> None:
        """Process the most recently collected number"""
        if not val:
            return
        if val[0] in DUP:
            # Run previous operation DUP[c] times. Note that it has been ran once already
            if not previousOperation:
                raise ValueError("DUP operation on DUP or DUP operation on nothing.")
            for _ in range(int(DUP[val[0]] + val[1:]) - 1):
                processNumber(previousOperation, None)
        elif val[0] in SQZ:
            dataInLine.append(float(SQZ[val[0]] + val[1:]))
        elif val[0] in DIF:
            if not dataInLine:
                raise ValueError("DIF operation on nothing")
            dataInLine.append(dataInLine[-1] + float(DIF[val[0]] + val[1:]))
        else:
            dataInLine.append(float(val))

    collectY: list[float] = []
    lastLineEndedDIF = False
    for line in XYYdata.split("\n"):
        current = ""
        previous = ""
        dataInLine: list[float] = []

        for c in line:
            if c.isdigit() or c == ".":
                # Number char, continue collection
                current += c
            elif c in SQZ or c in DIF or c in DUP or c == "-":
                # New number, process previous, store new
                processNumber(current, previous)
                if current:
                    previous = current
                current = c
            elif c in numberSpacerCharacters:
                # Process previous action
                processNumber(current, previous)
                if current:
                    previous = current
                    current = ""
            else:
                raise ValueError(f"Encountered unexpected {c} in {line}")
        # Store the last number
        processNumber(current, previous)

        # Store the data and perform the Y-check if the last entry on the previous line was DIF
        # X-data and checkpoints are discarded
        if lastLineEndedDIF:
            if len(dataInLine) < 2 or collectY[-1] != dataInLine[1]:
                raise ValueError(f"Failed Y-check for DIF on line {line}")
            collectY.extend(dataInLine[2:])
        else:
            collectY.extend(dataInLine[1:])

        # Y-check should only be performed if last Y-value was DIF
        lastLineEndedDIF = current and (
            current[0] in DIF or (current[0] in DUP and previous and previous[0] in DIF)
        )
    return np.array(collectY)


def _JCAMPshiftReference(
    val: str, freq: float, sw: float, nPoints: int, invertedAxis: bool
) -> Optional[float]:
    """Converts the JCAMP ##.SHIFT REFERENCE value to the 0 ppm frequency used by ssNake

    Args:
        val (str): the (unparsed) value of the ##.SHIFT REFERENCE key
        freq (float): the spectrometer offset frequency (Hz)
        sw (float): the spectrometer spectral width (Hz)
        nPoints (int): the number of points in the spectrum
        invertedAxis (bool): True if x-axis values are in order of decending frequency, False otherwise

    Returns:
        Optional[float]: _description_
    """
    splitVal = val.split(",")
    if len(splitVal) < 4:
        return None
    sr_dataPoint = int(splitVal[-2])  # The datapoint for the known shift (1-based)
    sr_ppmValue = float(splitVal[-1])  # The known shift value in ppm
    if sr_ppmValue is None or sr_dataPoint is None:
        return None

    df = sw / (nPoints - 1)
    if invertedAxis:
        df *= -1
    sr_HzValue = freq + df * ((sr_dataPoint - 1) - (nPoints - 1) / 2)
    return sr_HzValue / (1 + sr_ppmValue / 1e6)


def loadJCAMP(filePath: str) -> tuple:
    """Loads JCAMP-DX file.

    Parameters
    ----------
    filePath: string
        Path to the file that should be loaded

    Returns
    -------
    SpectrumClass
        SpectrumClass object of the loaded data
    """
    with open(filePath, "r") as f:
        data = f.read().split("\n")

    dataTypesOfInterest = (
        "NMR SPECTRUM",
        "NMR FID",
        "NMRSPECTRUM",
        "NMRFID",
    )  # No spaces encountered on older MestReNova-converted data
    endOfBlockKeys = ("END", "TITLE")
    dataTableKeys = ("XYDATA", "XYPOINTS", "PEAKTABLE", "ASSIGNMENTS", "DATATABLE")

    # ===============================================================
    # Step A: get key=value pairs for the (first) block with NMR data
    key = value = ""
    dataBlock: dict[str, Any] = {}
    currentPageBlock = None
    for line in data:
        # Remove comments
        if "$$" in line:
            line = line.split("$$", 1)[0]

        # Uniformize all whitespace to single spaces
        line = " ".join(line.strip().split())

        # Skip empty (or comment-only) lines
        if not line:
            continue

        # LDR, labelled data record
        if "=" in line and line.startswith("##"):
            # 1. Store previous LDR
            if key:
                if key == "PAGE":
                    currentPageBlock = value
                elif not currentPageBlock:
                    # Not inside a PAGE block (yet), store as normal (string) key
                    dataBlock[key] = value
                elif key not in dataBlock or isinstance(dataBlock[key], str):
                    # Either:
                    # - The keys inside the first PAGE: start building the tuple
                    # - nD dataset where e.g. ##FIRST is set in the overall block, but also in every PAGE block. The general one is redundant
                    #   and a string type, thus should be discarded in favor of the per-PAGE values, to be stored in tuples.
                    dataBlock[key] = (value,)
                else:
                    # Inside a PAGE block, add to values of previous PAGEs
                    dataBlock[key] = dataBlock[key] + (value,)

            # 2. Handle the new LDR
            key, value = line.split("=", 1)
            key = key[2:].upper().replace(" ", "")
            value = value.lstrip()

            # 3. Handle end of (previous) data blocks
            if key in endOfBlockKeys:
                if dataBlock.get("DATATYPE", "").upper() in dataTypesOfInterest:
                    # Currently we don't support multi-block datasets (e.g. 1 file with IR, 1H and 13C NMR spectra)
                    # Hence, abort after finding an NMR related one, rather than collecting further datasets.
                    break
                dataBlock = {}
                currentPageBlock = None
            if key == "ENDNTUPLES" and "PAGE" in dataBlock:
                currentPageBlock = None

        elif key in dataTableKeys:
            # Continued tables, keep newlines
            value += "\n" + line
        else:
            # Continued values
            value += " " + line

    if dataBlock.get("DATATYPE", "").upper() not in dataTypesOfInterest:
        raise Exception("Could not load JCAMP-DX NMR data: only 1-dimensional NMR data supported")

    # ====================================================================
    # Step B: get the important information keys and make them homogeneous
    # regardless of whether it was stored as tuple or XY-values
    spec = "FID" not in dataBlock["DATATYPE"].upper()
    freq = float(dataBlock.get(".OBSERVEFREQUENCY"))

    # Note: yFactor is optional
    nPoints = xUnits = firstX = lastX = yFactor = yData = None

    if dataBlock.get("DATACLASS", "").upper() == "NTUPLES" or dataBlock.get("NTUPLES"):
        # Data is stored as tuples
        # Assumption: X is the first column, Y/R/I follow, then other (meta)data
        RE_TUPLESEPARATOR = re.compile(r"[ ,]+")

        # Temporary get all the tuple datasets
        nPoints = [int(x) for x in re.split(RE_TUPLESEPARATOR, dataBlock.get("VAR_DIM", ""))]
        units = re.split(RE_TUPLESEPARATOR, dataBlock.get("UNITS", "").upper())
        first = [float(x) for x in re.split(RE_TUPLESEPARATOR, dataBlock.get("FIRST", ""))]
        last = [float(x) for x in re.split(RE_TUPLESEPARATOR, dataBlock.get("LAST", ""))]
        factor = [float(x) for x in re.split(RE_TUPLESEPARATOR, dataBlock.get("FACTOR", ""))]

        nPoints = nPoints[0] if nPoints and None not in nPoints else None
        xUnits = units[0] if units else None
        firstX = first[0] if first and None not in first else None
        lastX = last[0] if last and None not in last else None
        yFactor = factor[1:] if factor and None not in factor and len(factor) > 1 else None
        yFactor = cast(
            Optional[list[float]], yFactor
        )  # MyPy doesn't understand `None not in factor`

    # Ensure data tables are always tuples and get the first data table
    for datakey in ("DATATABLE", "XYDATA", "XYPOINTS"):
        data = dataBlock.get(datakey)
        if data:
            yData = (data,) if isinstance(data, str) else data
            break

    # If data wasn't stored as tuples, fall back to the non-tuple keys
    # yData and yFactor remain iterables, with the length of yData (or more)
    if nPoints is None:
        nPoints = int(dataBlock.get("NPOINTS"))
    if xUnits is None:
        xUnits = dataBlock.get("XUNITS", "").upper()
    if firstX is None:
        firstX = float(dataBlock.get("FIRSTX"))
    if lastX is None:
        lastX = float(dataBlock.get("LASTX"))
    if yFactor is None:
        factor = float(dataBlock.get("YFACTOR"))
        # Default to yFactor = 1.0
        yFactor = [factor if factor is not None else 1.0]

    if yData is None or nPoints is None or firstX is None or lastX is None or freq is None:
        raise Exception("Could not load JCAMP-DX NMR data: incomplete data")

    if len(yFactor) == 1 and len(yData) > 1:
        yFactor = yFactor * len(yData)

    # ===================================================================
    # STEP C: decode the data and combine real and imaginary if available
    spectDat = np.zeros(nPoints)
    for i, dataset in enumerate(yData):
        dataType, dataVal = dataset.split("\n", 1)
        # Assume X++(R..R) or X++(Y..Y) if not X++(I..I)
        # MestReNova data would need +1j, TopSpin and IUPAC testdata -1j
        multiplier = yFactor[i] * (-1j if "X++(I..I)" in dataType.upper() else 1)

        result = np.array([])

        try:
            # Try to convert ASDF data
            ASDFdata = convertASDF(dataVal)
            if ASDFdata.size == nPoints:
                result = ASDFdata
        except ValueError:
            pass
        if result.size == 0:
            # If AFFN data uses the E-notation for powers of 10, e.g. 3.14e22, the convertASDF
            # function will return incorrectly shaped data as e and E are SQZ digits.
            try:
                # Regular X Y ... Y form (AFFN)
                for dataline in dataVal.split("\n"):
                    result = np.append(result, np.fromstring(dataline, sep=" ")[1:])
            except ValueError:
                raise Exception("Could not load JCAMP-DX NMR data: unknown data encoding")

        if result.size == nPoints:
            spectDat = spectDat + result * multiplier
        else:
            raise Exception("Could not load JCAMP-DX NMR data: data size mismatch")

    # ============================
    # Step D: finalize the dataset
    freq = freq * 1e6
    ref = None

    if "$SF" in dataBlock:
        # This parameter only exists in TopSpin datasets, but provides the reference frequency also for FIDs
        ref = float(dataBlock["$SF"])
        if ref:
            ref *= 1e6

    if spec:
        sw = abs(firstX - lastX)
        sw = sw + sw / nPoints
        if ".SHIFTREFERENCE" in dataBlock:
            ref = _JCAMPshiftReference(
                dataBlock[".SHIFTREFERENCE"],
                freq=freq,
                sw=sw,
                nPoints=nPoints,
                invertedAxis=(firstX > lastX),
            )
        if ref is None:
            ref = freq - (firstX + lastX) / 2
        if xUnits != "PPM":
            firstX /= ref
            lastX /= ref
    else:
        # FID [seconds]
        sw = 1.0 / ((lastX - firstX) / (nPoints - 1))

    # Convert sw to units of ppm if it isnt already
    if xUnits != "PPM":
        sw *= 10**6 / ref

    # Convert y-data to spectrum intensities in the order of ascending corresponding x-values
    if spec:
        if firstX > lastX:
            spectDat = spectDat[::-1]
    else:
        # The data is not in spectral form, so it needs to be fourier transformed
        spectDat = np.fft.fftshift(np.fft.fft(spectDat))

    # Construct the x-axis in ppm units from sw, freq and ref in Hz.
    firstX = -sw / 2 + 10**6 * (freq - ref) / ref
    lastX = sw / 2 + 10**6 * (freq - ref) / ref
    xAxis = np.linspace(firstX, lastX, nPoints)

    # Include the observed isotope to label the x-axis correctly:
    isotope = dataBlock.get(".OBSERVENUCLEUS")

    return xAxis, spectDat, isotope
