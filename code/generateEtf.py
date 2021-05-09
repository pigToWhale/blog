import json
import collections

theTags=[]
etfFile=""

def dumpStruct():
    return f"# List of ETFs\n\n"

def dumpSector():
    return f"# List of Sectors\n\n"

def getEtfListForWrite(iEtfRaw):
    etfFile=""
    for etf in iEtfRaw:
        etfFile = etfFile + "## " + etf['name'] + "\n" + etf['description'] + "\n\n"
    return etfFile

def getEtfMatchingSector(iEtfsRaw, iOneSector):
    aMatchingEtfs=[]
    for aOneEtf in iEtfsRaw:
        #print (f"sector tags {iOneSector['tags']} and etf tags {aOneEtf['tags']}")
        if all(tag in aOneEtf["tags"] for tag in iOneSector["tags"]):
            print(f"ETF {aOneEtf['name']} match sector {iOneSector['theme']}")
            aMatchingEtfs.append(aOneEtf)
    return aMatchingEtfs

def getSectorListForWrite(iSectorRaw, iEtfsRaw):
    SectorContent=""
    for aOneSector in iSectorRaw:
        SectorContent = SectorContent + "## " + aOneSector['theme'] + "\n" + aOneSector['description'] + "\n\n"
        # Find the ETF for this sector
        SectorContent = SectorContent + "### Matching ETFs: " + "\n"
        aMatchinEtfs = getEtfMatchingSector(iEtfsRaw, aOneSector)
        for aOneMatchingEtf in aMatchinEtfs:
            SectorContent = SectorContent + f"* {aOneMatchingEtf['name']} \n"
        SectorContent = SectorContent + "\n\n"
    return SectorContent

def writeOutputFile(iDestFile, iContent):
    f = open("../etf.md", "w")
    aTextToWrite=dumpStruct()
    aTextToWrite=aTextToWrite + getEtfListForWrite(iContent)
    f.write(aTextToWrite)
    f.close()

def writeSectorOutputFile(iDestFile, iSectorsRaw, iEtfsRaw):
    f = open(iDestFile, "w")
    aTextToWrite=dumpSector()
    aTextToWrite=aTextToWrite + getSectorListForWrite(iSectorRaw = iSectorsRaw,iEtfsRaw=iEtfsRaw)
    f.write(aTextToWrite)
    f.close()

def processEtfJson(iSrcFile):
    with open(iSrcFile) as json_file:
        data = json.load(json_file)
        return data

def processSectorJson(iSrcFile):
    with open(iSrcFile) as json_file:
        data = json.load(json_file)
        return data

aEtfsRaw = processEtfJson("../etf.json")
aSectorsRaw = processSectorJson("../sectors.json")

writeOutputFile("../etfs.md", aEtfsRaw)
writeSectorOutputFile(iDestFile = "../sectors.md", iSectorsRaw = aSectorsRaw,iEtfsRaw = aEtfsRaw)
