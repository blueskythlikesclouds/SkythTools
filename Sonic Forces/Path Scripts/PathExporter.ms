-- Forces Path Exporter by Radfordhound
-- Built on LWPathImporter by arukibree
fileIn "IO.ms"

global GlobalUp = [0,1,0]
global yzflip = true
global MeterScale = 10
global Version = 1 -- 0: Wii U / 1: PC

offset_array = #()
fn addOffset f = (
	append offset_array (ftell f)
)

-- String Table "class"
struct StringEntry (
	str, addresses
)
StringEntries = #()

fn AddString f str = (
	unique = true
	
	for s = 1 to StringEntries.count do (
		if (StringEntries[s].str == str) then (
			append StringEntries[s].addresses (ftell f)
			unique = false
			exit
		)
	)
	
	if (unique == true) then (
		entry = StringEntry str:str addresses:#(ftell f)
		append StringEntries entry
	)
	
	WriteLongLongLE f 0 #unsigned
)

fn WriteTable f = (
	for s = 1 to StringEntries.count do (
		offset = ftell f
		
		for a = 1 to StringEntries[s].addresses.count do (
			fseek f StringEntries[s].addresses[a] #seek_set
			WriteLongLE f (offset - 0x40) #unsigned
		)
		
		fseek f offset #seek_set
		WriteString f StringEntries[s].str
	)
)

-- Point3 Util
fn MidPoint v1 v2 = (
	v = (v2 - v1) * 0.5
	return (v1 + v)
)

fn DirectionTo v1 v2 = (
	return normalize (v2 - v1)
)

fn WritePoint3 f P3 = (
	WriteFloatLE f P3.x
	WriteFloatLE f P3.y
	WriteFloatLE f P3.z
)

-- String Util
fn TagFromName str = (
	at_index = (str.count - 2)
	format "ind %\n" at_index
	format "ch %\n" str[at_index]
	if (str.count < at_index or str[at_index] != "_") then return undefined
	return substring str (at_index + 1) (str.count - at_index)
)

fn NameWithoutTag str = (
	at_index = (str.count - 2)
	if (str.count < at_index or str[at_index] != '_') then return undefined
	return substring str 1 (at_index - 1)
)

fn HasPartTag str = (
	tag = TagFromName str
	if (tag == undefined) then return false
	if ((substring tag 1 2) == "pt") then return true
	else return false
)

fn GetPartNumber str = (
	tag = TagFromName str
	if (tag == undefined) then return undefined
	if ((substring tag 1 2) != "pt") then return undefined
	
	StrNum = substring tag 3 (tag.count - 2)
	if (StrNum == "") then return undefined
	
	return StrNum as integer
)

fn GetPathID str = (
	num_index = FindString str "_"
	if (num_index == undefined) then return 0
	num_str = substring str (num_index + 1) (str.count - num_index + 3)
	num = (num_str as integer)
	format "Path ID for % : %\n" str num
	return num
)

fn GetSVPathID str = (
	num_index = FindString str "_"
	if (num_index == undefined) then return 0
	num_str = substring str (num_index - 3) 3
	num = (num_str as integer) + 1000
	format "SV Path ID for % : %\n" str num
	return num
)

-- Path
struct LWPath (
	Name, Knots, DoubleKnots, IsDouble, Type, BBMin, BBMax
)

fn ShapeToLWPath SrcShape = (
	
	NewPath = LWPath()
	NewPath.Name = SrcShape.name
	NewPath.Knots = #()
	NewPath.DoubleKnots = #()
	NewPath.Type = TagFromName NewPath.Name
	NewPath.BBMin = [99999999, 99999999, 99999999]
	NewPath.BBMax = [-99999999, -99999999, -99999999]
	
	-- Create knots + construct bounding box
	-- Single spline
	if ((NumSplines SrcShape) == 1) then (
		NewPath.IsDouble = false
	
		for k = 1 to (NumKnots SrcShape) do (
			Knot = (GetKnotPoint SrcShape 1 k) * MeterScale
			if (yzflip == true) then Knot = [Knot.x, Knot.z, -Knot.y]
			append NewPath.Knots Knot
			
			if (Knot.x < NewPath.BBMin.x) then NewPath.BBMin.x = Knot.x
			if (Knot.y < NewPath.BBMin.y) then NewPath.BBMin.y = Knot.y
			if (Knot.z < NewPath.BBMin.z) then NewPath.BBMin.z = Knot.z
			if (Knot.x > NewPath.BBMax.x) then NewPath.BBMax.x = Knot.x
			if (Knot.y > NewPath.BBMax.y) then NewPath.BBMax.y = Knot.y
			if (Knot.z > NewPath.BBMax.z) then NewPath.BBMax.z = Knot.z
		)
	)
	
	-- Double spline
	else if (NumSplines SrcShape == 2) then (
		NewPath.IsDouble = true
		
		-- For double splines, the knot count needs to match on both splines
		if ((NumKnots SrcShape 1) != (NumKnots SrcShape 2)) then (
			MessageBox("Error: " + SrcShape.name + " is a double spline, but the splines have a different knot count")
			return undefined
		)
		
		for k = 1 to (NumKnots SrcShape 1) do (
			KnotA = (GetKnotPoint SrcShape 1 k) * MeterScale
			KnotB = (GetKnotPoint SrcShape 2 k) * MeterScale
			
			if (yzflip == true) then (
				KnotA = [KnotA.x, KnotA.z, -KnotA.y]
				KnotB = [KnotB.x, KnotB.z, -KnotB.y]
			)
			
			MidKnot = MidPoint KnotA KnotB
			append NewPath.Knots MidKnot
			append NewPath.DoubleKnots KnotA
			append NewPath.DoubleKnots KnotB
			
			if (KnotA.x < NewPath.BBMin.x) then NewPath.BBMin.x = KnotA.x
			if (KnotA.y < NewPath.BBMin.y) then NewPath.BBMin.y = KnotA.y
			if (KnotA.z < NewPath.BBMin.z) then NewPath.BBMin.z = KnotA.z
			if (KnotA.x > NewPath.BBMax.x) then NewPath.BBMax.x = KnotA.x
			if (KnotA.y > NewPath.BBMax.y) then NewPath.BBMax.y = KnotA.y
			if (KnotA.z > NewPath.BBMax.z) then NewPath.BBMax.z = KnotA.z
			
			if (KnotB.x < NewPath.BBMin.x) then NewPath.BBMin.x = KnotB.x
			if (KnotB.y < NewPath.BBMin.y) then NewPath.BBMin.y = KnotB.y
			if (KnotB.z < NewPath.BBMin.z) then NewPath.BBMin.z = KnotB.z
			if (KnotB.x > NewPath.BBMax.x) then NewPath.BBMax.x = KnotB.x
			if (KnotB.y > NewPath.BBMax.y) then NewPath.BBMax.y = KnotB.y
			if (KnotB.z > NewPath.BBMax.z) then NewPath.BBMax.z = KnotB.z
		)
	)
	
	-- More than 2? Invalid
	else (
		if (NumSplines SrcShape == 0) then (
			MessageBox("Error: " + SrcShape.name + " cannot be exported because it has no splines")
		)
		else MessageBox("Error: " + SrcShape.name + " cannot be exported because it has more than two splines")
		
		return undefined
	)
	
	-- Finished
	return NewPath
)

fn ComparePath p1 p2 = (
	if (p1.Name < p2.Name) then return -1
	if (p1.Name == p2.Name) then return 0
	if (p1.Name > p2.Name) then return 1
)

-- Main script
path_file = getSaveFileName caption:"Save paths" types:"Sonic Forces Path (*.path)|*.path"

if (path_file != undefined) do (
	f = fopen path_file "wb"
	
	if (version == 0) then SetBigEndian()
	else if (version == 1) then SetLittleEndian()
	
	-- Create paths
	PathArray = #()
	for p in selection where (isKindOf p shape) do (
		NewPath = ShapeToLWPath p
		
		if (NewPath != undefined) then append PathArray NewPath
	)
	qsort PathArray ComparePath
	PathCount = PathArray.count
	
	-- Start writing
	NextAvailableID = 1
	
	-- BINA Header
	WriteLongBE f 0x42494E41 #unsigned -- BINA
	WriteLongBE f 0x3231304C #unsigned -- 210L
	WriteLongBE f 0 #unsigned -- File Size (Fill in later)
	WriteShortLE f 1 #unsigned
	WriteShortLE f 0 #unsigned
	WriteLongBE f 0x44415441 #unsigned -- DATA
	WriteLongBE f 0 #unsigned -- DATA Size (Fill in later)
	WriteLongBE f 0 #ungisned -- String Table Offset (Fill in later)
	WriteLongBE f 0 #unsigned -- String Table Length (Fill in later)
	WriteLongBE f 0 #unsigned -- Final Table Length (Fill in later)
	
	WriteLongLE f 0x18 #unsigned
	WriteLongLongLE f 0 #unsigned
	WriteLongLongLE f 0 #unsigned
	WriteLongLongLE f 0 #unsigned
	
	-- Header
	WriteLongLE f 0x50415448 #unsigned -- "PATH" magic
	WriteShortLE f 0x200 #unsigned
	WriteShortLE f 0 #unsigned
	WriteLongLongLE f PathCount #unsigned
	addOffset f
	WriteLongLongLE f 0x18 #unsigned
	
	-- Path headers - first pass, enter junk. We'll write this later. The only thing we'll do now is add strings/offsets.
	for iPath = 1 to PathCount do (
		p = PathArray[iPath]
		
		start = (ftell f)
		addOffset f
		AddString f p.Name
		
		append offset_array (start + 0x10)
		append offset_array (start + 0x18)
		append offset_array (start + 0x20)
		append offset_array (start + 0x28)
		append offset_array (start + 0x30)
		if (p.IsDouble == true) then append offset_array (start + 0x40)
		append offset_array (start + 0x68)
		append offset_array (start + 0x78)
		
		-- Write temp junk
		for i = 1 to 30 do WriteLongLE f 0 #unsigned
	)
	
	-- Actual path data
	for iPath = 1 to PathCount do (
		p = PathArray[iPath]
		
		-- Bool Array
		-- I don't know what this does, but setting everything to 0 has no noticeable effect
		BoolsOffset = ftell f
		
		for k = 1 to p.Knots.count do WriteByte f 0
		while ((mod (ftell f) 4) != 0) do WriteByte f 0
		
		-- Dist Array
		DistOffset = ftell f
		dist = 0
		
		for k = 1 to p.Knots.count do (
			if (k > 1) then dist += distance p.Knots[k] p.Knots[k-1]
			WriteFloatLE f dist
		)
		
		PathLength = dist
		
		-- Knot Array
		KnotsOffset = ftell f
		
		for k = 1 to p.Knots.count do (
			WritePoint3 f p.Knots[k]
		)
		
		-- Up Vector Array
		UpVecsOffset = ftell f
		last = GlobalUp
		
		for k = 1 to p.Knots.count do (
			if (k == p.Knots.count) then WritePoint3 f last
			
			else (
				-- Calculating the up vector is done differently for single splines than it is for double
				
				-- Single Spline
				if (p.IsDouble == false) then (
					knot = p.Knots[k]
					next = p.Knots[k+1]
					
					forward = DirectionTo knot next
					right = normalize (Cross forward last)
					up = normalize (Cross right forward)
					WritePoint3 f up
					
					last = up
				)
				
				-- Double Spline
				else (
					KnotIndex = ((k - 1) * 2) + 1
					
					knotA = p.DoubleKnots[KnotIndex]
					knotB = p.DoubleKnots[KnotIndex+1]
					nextA = p.DoubleKnots[KnotIndex+2]
					
					forward = DirectionTo knotA nextA
					right = DirectionTo knotA knotB
					up = normalize (Cross right forward)
					WritePoint3 f up
					
					last = up
				)
			)
		)
		
		-- Forward Vector Array
		ForwardVecsOffset = ftell f
		last = [1,0,0]
		
		for k = 1 to p.Knots.count do (
			if (k == p.Knots.count) then WritePoint3 f last
			
			-- The forward vector can be calculated the same way for both types
			else (
				knot = p.Knots[k]
				next = p.Knots[k+1]
				
				forward = DirectionTo knot next
				WritePoint3 f forward
				
				last = forward
			)
		)
		
		-- Double Spline Knot Array
		DoubleSplineOffset = ftell f
		
		if (p.IsDouble == true) then (
			for k = 1 to p.DoubleKnots.count do (
				WritePoint3 f p.DoubleKnots[k]
			)
		)
		
		else DoubleSplineOffset = 0
		
		-- Metadata
		while ((mod (ftell f) 8) != 0) do WriteByte f 0
		MetaOffset = ftell f
		MetaCount = 0
		
		-- Evaluate spline type
		local type = 0
		format "Type %\n" p.Type
		if (p.Type == "SV") then type = 1
		if (p.Type == "GR") then type = 2
		if (p.Type == "GR_spd1") then type = 2
		if (p.Type == "GR_spd2") then type = 2
		if (p.Type == "GR_spd3") then type = 2
		
		-- Write metadata
		-- "type" field present for all types
		append offset_array (ftell f)
		AddString f "type"
		WriteLongLongLE f 0 #unsigned
		WriteLongLongLE f type #unsigned
		MetaCount += 1
		
		-- "uid" field present for type 0
		if (type == 0) then (
			append offset_array (ftell f)
			AddString f "uid"
			WriteLongLongLE f 0 #unsigned
			WriteLongLongLE f (GetPathID p.Name) #unsigned
			
			MetaCount += 1
		)
		
		-- SV Path UUIDs
		if (type == 1) then
		(
			append offset_array (ftell f)
			AddString f "uid"
			WriteLongLongLE f 0 #unsigned
			WriteLongLongLE f (GetSVPathID p.Name) #unsigned
			
			MetaCount += 1
		)
		
		-- "next" field present for type 0 @ptX
		-- this is a little tricky - need to identify the next subsequent part
		if (HasPartTag p.Name == true) then (
			PartNum = GetPartNumber p.Name
			
			for i = 1 to PathArray.count do (
				if (HasPartTag PathArray[i].Name == true) then (
					OtherNum = GetPartNumber PathArray[i].Name
					
					if (OtherNum == PartNum + 1) then (
						append offset_array (ftell f)
						AddString f "next"
						WriteLongLongLE f 0x02000000 #unsigned
						append offset_array (ftell f)
						AddString f PathArray[i].Name
						MetaCount += 1
						exit
						
					)
				)
			)
		)
		
		-- "grind_speed" field present for type 2
		/*if (type == 2) then (
			append offset_array (ftell f)
			AddString f "grind_speed"
			WriteLongLE f 0 #unsigned
			
			if (p.Type == "GR") then WriteLongLE f 0 #unsigned -- Default to regular
			else if (p.Type == "GR_spd1") then WriteLongLE f 1 #unsigned -- Slow
			else if (p.Type == "GR_spd2") then WriteLongLE f 0 #unsigned -- Regular
			else if (p.Type == "GR_spd3") then WriteLongLE f 2 #unsigned -- Fast
			
			MetaCount += 1
		)*/
		
		-- KD tree
		-- The exact structure of this part is unknown, but luckily we can cheat our way through this part.
		-- There are no noticeable ingame issues from doing it this way; it's likely only a very small performance hit
		KDTreeOffset = ftell f
		
		local NumLineSegments
		if (p.IsDouble == true) then NumLineSegments = p.DoubleKnots.count - 2
		else NumLineSegments = p.Knots.count - 1
		
		WriteLongLE f 0 #unsigned
		WriteLongLE f 2 #unsigned
		append offset_array (ftell f)
		WriteLongLongLE f ((KDTreeOffset + 0x30) - 0x40) #unsigned
		
		WriteLongLongLE f 1 #unsigned
		append offset_array (ftell f)
		WriteLongLongLE f ((KDTreeOffset + 0x40) - 0x40) #unsigned
		
		WriteLongLongLE f NumLineSegments #unsigned
		append offset_array (ftell f)
		WriteLongLongLE f ((KDTreeOffset + 0x48) - 0x40) #unsigned
		
		-- The first data section is the unknown bit
		WriteLongLE f 0 #unsigned
		WriteLongLE f 0 #unsigned
		WriteLongLE f 3 #unsigned
		WriteLongLE f 0 #unsigned
		
		-- The second bit assigns line segments to... something.
		-- [count] int pairs - first is count, second is starting index.
		-- eg "add 6 segments staring from segment 7"
		WriteLongLongLE f NumLineSegments #unsigned
		
		-- The third bit seems to be just line segment indices/IDs
		for i = 1 to NumLineSegments do WriteLongLE f (i - 1) #unsigned
		
		while ((mod (ftell f) 8) != 0) do WriteByte f 0
		
		-- Done with path data - now backtrack and write path header
		PathDataEnd = ftell f
		HeaderOffset = 0x58 + (0x80 * (iPath - 1))
		fseek f HeaderOffset #seek_set
		
		-- Path Header
		--format "Writing path header % at 0x%\n" iPath (bit.intashex (ftell f))
		WriteLongLongLE f 0 #unsigned -- This is the name offset; will be filled in by the WriteTable() call later
		WriteByte f 0x1 #unsigned -- Unknown value, always 0x1
		WriteByte f 0x0 #unsigned -- Unknown value, always 0x0
		WriteShortLE f p.Knots.count #unsigned
		WriteFloatLE f PathLength
		WriteLongLongLE f (BoolsOffset - 0x40) #unsigned
		WriteLongLongLE f (DistOffset - 0x40) #unsigned
		WriteLongLongLE f (KnotsOffset - 0x40) #unsigned
		WriteLongLongLE f (UpVecsOffset - 0x40) #unsigned
		WriteLongLongLE f (ForwardVecsOffset - 0x40) #unsigned
		WriteLongLongLE f (p.DoubleKnots.count) #unsigned
		if (DoubleSplineOffset != 0) then WriteLongLongLE f (DoubleSplineOffset - 0x40) #unsigned
		else WriteLongLongLE f 0 #unsigned
		WritePoint3 f p.BBMin
		WritePoint3 f p.BBMax
		WriteLongLongLE f MetaCount #unsigned
		WriteLongLongLE f (MetaOffset - 0x40) #unsigned
		WriteLongLongLE f 0 #unsigned -- Unknown value, always 0
		WriteLongLongLE f (KDTreeOffset - 0x40) #unsigned
		
		fseek f PathDataEnd #seek_set
	)
	
	-- Write String and Offset Table
	local stringTablePos = (ftell f)
	WriteTable f
	while ((mod (ftell f) 4) != 0) do WriteByte f 0
	
	local footerStartPos = (ftell f)
	local lastOffsetPos = 0x40
	for o = 1 to offset_array.count do
	(
		local offset = offset_array[o]
		
		d = (bit.shift (offset - lastOffsetPos) -2); -- >> 2
		if (d <= 0x3F) then
		(
			-- 0x40 | d
			WriteByte f (bit.or 0x40 d) #unsigned
		)
		else if (d <= 0x3FFF) then
		(
			-- (0x80 << 8) | d
			WriteShortBE f (bit.or (bit.shift 0x80 8) d) #unsigned
		)
		else
		(
			-- (0xC0 << 24) | d
			WriteLongBE f (bit.or (bit.shift 0xC0 24) d) #unsigned
		)
		
		lastOffsetPos = offset
	)
	
	-- Fix Padding
	while ((mod (ftell f) 4) != 0) do WriteByte f 0
	fileSize = (ftell f)
	
	-- Fill-In Header Values
	fseek f 0x8 #seek_set
	WriteLongLE f fileSize #unsigned -- File Size
	fseek f 0x8 #seek_cur
	WriteLongLE f (fileSize - 0x10) #unsigned -- DATA Size
	
	WriteLongLE f (stringTablePos - 0x40) #unsigned -- String Table Offset
	WriteLongLE f (footerStartPos - stringTablePos) #unsigned -- String Table Size
	WriteLongLE f (fileSize - footerStartPos) #unsigned -- Offset Table Size

	-- Finished
	fclose f
)