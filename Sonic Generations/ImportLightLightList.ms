-- Sonic Generations .light importer

clearListener()

yzflip = true

fn floatSwap2 f = (
	i = bit.floatAsInt f
	h = bit.intashex i
	while h.count < 8 do h = "0" + h
	
	s = (substring h 7 2) + (substring h 5 2) + (substring h 3 2) + (substring h 1 2)
	bit.intAsFloat (bit.hexasint s)
)	

fn ReadBElong fstream = (
long = readlong fstream
long = bit.swapBytes long 1 4
long = bit.swapBytes long 2 3
if long != undefined then return long
	else return 0
)

fn ReadBEFloat fstream = (
return floatSwap2(readfloat fstream)
)

fn ImportLight lightfile = (
	LightName = getFilenameFile lightfile
	f = fopen lightfile "rb"
	
	fseek f 0x18 #seek_set
	LightType = ReadBELong f
	
	-- LightType 0 = Directional Light
	if LightType == 0 then (
		if yzflip == true then (
			TargetX = ReadBEFloat f
			TargetZ = ReadBEFloat f
			TargetY = -(ReadBEFloat f)
		)	
		if yzflip == false then (
			TargetX = ReadBEFloat f
			TargetY = ReadBEFloat f
			TargetZ = ReadBEFloat f
		)
		R = (ReadBEFloat f) * 255
		G = (ReadBEFloat f) * 255
		B = (ReadBEFloat f) * 255
		SGLight = TargetDirectionalLight	target:(targetobject pos:[TargetX, TargetY, TargetZ]) rgb:[R, G, B]
		SGLight.name = LightName
		SGLight.target.name = LightName + ".Target"
	)
	
	--LightType 1 = Omni Light
	if LightType == 1 then (
		if yzflip == true then (
			PosX = ReadBEFloat f
			PosZ = ReadBEFloat f
			PosY = -(ReadBEFloat f)
		)
		if yzflip == false then (
			PosX = ReadBEFloat f
			PosY = ReadBEFloat f
			PosZ = ReadBEFloat f
		)
		R = (ReadBEFloat f) * 255
		G = (ReadBEFloat f) * 255
		B = (ReadBEFloat f) * 255
		decay = ReadBEFloat f
		near_atten_start = ReadBEFloat f
		near_atten_end = ReadBEFloat f
		far_atten_start = ReadBEFloat f
		far_atten_end = ReadBEFloat f
		
		SGLight = OmniLight pos:[PosX, PosY, PosZ] rgb:[R, G, B]  decayRadius:decay useNearAtten:true nearAttenStart:near_atten_start nearAttenEnd:near_atten_end useFarAtten:true farAttenStart:far_atten_start farAttenEnd:far_atten_end
		SGLight.name = LightName
	)
)

lightname = GetOpenFileName caption:"Open Light File" types:"Hedgehog Engine Light (*.light, *.light-list)|*.light;*.light-list"

if (lightname != undefined) and ((doesFileExist lightname) == true) do (
	FileExt = getFilenameType lightname

	if FileExt == ".light" then ImportLight lightname
	if FileExt == ".light-list" then (
		f = fopen lightname "rb"
		fseek f 0x18 #seek_set
		light_count = ReadBELong f
		light_table_offset = ReadBELong f
		
		light_offsets = #()
		for l = 1 to light_count do (
			light_offsets[l] = (ReadBELong f) + 0x18
		)
		
		light_list = #()
		for l = 1 to light_count do (
			fseek f light_offsets[l] #seek_set
			LightName = ReadString f
			ImportLight (LightName + ".light")
		)
	)
)
