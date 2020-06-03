import clr

# List for hardware types and sensor types that our DLL can open
OHM_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']
OHM_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData']


class cpuInfo():
    def __init__(self, pathDll):
        if pathDll is not None:
            self.hw = self.init_OHM(pathDll)

    def init_OHM(self, pathDll):
        clr.AddReference(pathDll)
        from OpenHardwareMonitor import Hardware
        hw = Hardware.Computer()
        hw.MainboardEnabled, hw.CPUEnabled, hw.RAMEnabled, hw.GPUEnabled, hw.HDDEnabled = False, True, False, False, False
        hw.Open()
        return hw

    def fetch_data(self):
        out = []
        for i in self.hw.Hardware:
            i.Update()
            for sensor in i.Sensors:
                thing = self.parse_sensor(sensor)
                if thing is not None:
                    out.append(thing)
            for j in i.SubHardware:
                j.Update()
                for subsensor in j.Sensors:
                    thing = self.parse_sensor(subsensor)
                    out.append(thing)
        return out

    def parse_sensor(self, sensor):
        HwType = OHM_hwtypes[sensor.Hardware.HardwareType]
        SensorType = OHM_sensortypes[sensor.SensorType]
        if "total" in sensor.Name.lower():
            return {"Type": HwType, "Name": sensor.Hardware.Name, "Sensor": sensor.Name, "SensorType": SensorType, "Reading": sensor.Value}

