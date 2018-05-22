
import subprocess


script_path = "/home/pi/CuraEngine/build/CuraEngine"

args = []
args.append(script_path)
args.append("slice")
args.append("-j")
args.append("simple.json")
# This is something that our other slicer code sets in a more
# sophisticated way, perhaps.
args.append("-s")
args.append("line_width=0.3")
args.append("-o")
args.append("xyzCuraTest.gcode")
args.append("-l")
args.append("xyzCalibration_cube.stl")

print args
try:
    my_result = subprocess.check_output(args, stderr=subprocess.STDOUT)

except subprocess.CalledProcessError as e:
    print("something went wrong")
    my_result = e.output


print my_result




