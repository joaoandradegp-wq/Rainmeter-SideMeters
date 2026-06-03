function Initialize()
    path = "C:\\Users\\phobos\\Documents\\Rainmeter\\network_status.txt"
end

function Update()
    local file = io.open(path, "r")
    if not file then
        return
    end

    local lines = {}

    for line in file:lines() do
        table.insert(lines, line)
    end

    file:close()

    if lines[1] then
        SKIN:Bang("!SetOption", "meterPC1Status", "Text", lines[1])
        if lines[1] == "ONLINE" then
            SKIN:Bang("!SetOption", "meterPC1Status", "FontColor", "0,255,0,255")
        else
            SKIN:Bang("!SetOption", "meterPC1Status", "FontColor", "255,80,80,255")
        end
    end

    if lines[2] then
        SKIN:Bang("!SetOption", "meterPC2Status", "Text", lines[2])
        if lines[2] == "ONLINE" then
            SKIN:Bang("!SetOption", "meterPC2Status", "FontColor", "0,255,0,255")
        else
            SKIN:Bang("!SetOption", "meterPC2Status", "FontColor", "255,80,80,255")
        end
    end

    if lines[3] then
        SKIN:Bang("!SetOption", "meterPC3Status", "Text", lines[3])
        if lines[3] == "ONLINE" then
            SKIN:Bang("!SetOption", "meterPC3Status", "FontColor", "0,255,0,255")
        else
            SKIN:Bang("!SetOption", "meterPC3Status", "FontColor", "255,80,80,255")
        end
    end

    if lines[4] then
        SKIN:Bang("!SetOption", "meterPC4Status", "Text", lines[4])
        if lines[4] == "ONLINE" then
            SKIN:Bang("!SetOption", "meterPC4Status", "FontColor", "0,255,0,255")
        else
            SKIN:Bang("!SetOption", "meterPC4Status", "FontColor", "255,80,80,255")
        end
    end

    if lines[5] then
        SKIN:Bang("!SetOption", "meterPC5Status", "Text", lines[5])
        if lines[5] == "ONLINE" then
            SKIN:Bang("!SetOption", "meterPC5Status", "FontColor", "0,255,0,255")
        else
            SKIN:Bang("!SetOption", "meterPC5Status", "FontColor", "255,80,80,255")
        end
    end

    if lines[6] then
        SKIN:Bang("!SetOption", "meterPC6Status", "Text", lines[6])
        if lines[6] == "ONLINE" then
            SKIN:Bang("!SetOption", "meterPC6Status", "FontColor", "0,255,0,255")
        else
            SKIN:Bang("!SetOption", "meterPC6Status", "FontColor", "255,80,80,255")
        end
    end

    SKIN:Bang("!UpdateMeter", "*")
    SKIN:Bang("!Redraw")
end