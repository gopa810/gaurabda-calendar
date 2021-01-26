from . import GCMath as GCMath

def GetRasi(SunLongitude,Ayanamsa):
	return int(GCMath.Floor(GCMath.putIn360(SunLongitude - Ayanamsa)/30.0))
