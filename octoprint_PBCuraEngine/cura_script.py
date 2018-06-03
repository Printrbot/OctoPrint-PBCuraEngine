
import subprocess
import json

script_path = "/home/pi/CuraEngine/build/CuraEngine"

args = []
args.append(script_path)
args.append("slice")

# I've tried to package JSON inline with the .cmd an it doesn't work.
# the script wants a file.

args.append("-j")
args.append("./profiles/fdmprinter.def.json")


# Not using this for now.
#param = open('./simple_full.json', 'r')
#param_list = json.load(param)
#for key in param_list.keys():
#    args.append("-s")
#    args.append(key.encode("ascii") + "=" + param_list[key].encode("ascii"))
#args.append("-j")
#args.append(json.dumps(param_list))

args.append("-v") # verbose logging
args.append("-p") # log progress
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




