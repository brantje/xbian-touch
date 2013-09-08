from uinputmapper.cinput import *
mport subprocess

#Read screen resolution from tvservice (not framebuffer)
sres = subprocess.check_output("tvservice -s", shell=True)
sres = sres.split(", ")
sres = sres[1].split(" @")
sres = sres[0].split("x")
xsres = int(sres[0])
ysres = int(sres[1])
xmres = 1280
ymres = 720

if xsres >= xmres:
    xsres = xmres
    ysres = ymres

# Read ts_calibrate data from /etc/pointercal
filename = "/etc/pointercal"
data = []
with open(filename, "r") as f:
    for val in f.read().split():
        data.append(int(val))
f.close()

xymix = data[0]
xscale = data[1]
xoffset = data[2]
yscale = data[3]
yxmix = data[4]
yoffset = data[5]
scaler = data[6]
xres = data[7]
yres = data[8]
swap = data[9]

xcalib = xsres / float(xres)
ycalib = ysres / float(yres)

if swap == 0:
    xymix, xscale = xscale, xymix
    yxmix, yscale = yscale, yxmix

#print xscale, xymix, xoffset, yxmix, yscale, yoffset, scaler, xres, yres, swap

def transform_x(x):
    x = (x*xscale + xoffset)*xcalib/(scaler) + (xmres - xsres)
    return int(x)

def transform_y(y):
    y = (y*yscale + yoffset)*ycalib/(scaler) + (ymres - ysres)
    return int(y)

x_value = transform_x
y_value = transform_y

X_ABS = ABS_X
Y_ABS = ABS_Y
X_ABS_MT_POSITION = ABS_MT_POSITION_X
Y_ABS_MT_POSITION = ABS_MT_POSITION_Y

if swap == 1:
    X_ABS, Y_ABS = Y_ABS, X_ABS
    X_ABS_MT_POSITION, Y_ABS_MT_POSITION = Y_ABS_MT_POSITION, X_ABS_MT_POSITION
    x_value, y_value = y_value, x_value

config = {
        (0, EV_ABS) : {
            ABS_X : {
                'type' : (0, EV_ABS),
                'code' : X_ABS,
                'value' : x_value,
                'prop' : {
                    'max' : 2047,
                    'min' : 0,
                    'flat' : 0,
                    'fuzz' : 0
                }
            },
            ABS_Y : {
                'type' : (0, EV_ABS),
                'code' : Y_ABS, 
                'value' : y_value, 
                'prop' : {
                    'max' : 2047,
                    'min' : 0,
                    'flat' : 0,
                    'fuzz' : 0
                }
            },
            ABS_MT_POSITION_X : {
                'type' : (0, EV_ABS),
                'code' : X_ABS_MT_POSITION,
                'value' : x_value,
                'prop' : {
                    'max' : 2047,
                    'min' : 0,
                    'flat' : 0,
                    'fuzz' : 0
                }
            },
            ABS_MT_POSITION_Y : {
                'type' : (0, EV_ABS),
                'code' : Y_ABS_MT_POSITION,
                'value' : y_value,
                'prop' : {
                    'max' : 2047,
                    'min' : 0,
                    'flat' : 0,
                    'fuzz' : 0
                }
            }
        },
        (0, EV_KEY): {
            BTN_RIGHT: {
                'type' : (0, EV_KEY),
                'code' : BTN_RIGHT,
                'value' : lambda x: 0 if x == 0 else 1
            }
        },
        (0, EV_KEY): {
            KEY_RIGHT: {
                'type' : (0, EV_KEY),
                'code' : KEY_RIGHT,
                'value' : lambda x: 0 if x == 0 else 1
            }
        }
}

def config_merge(c):
    # XXX: We cannot just use update; as it will override everything in say EV_KEY
    for k, v in config.iteritems():
        if k in c:
            c[k].update(v)
        else:
            c[k] = v

    # Uncomment this to make touch click too
    
    #c[(0, EV_KEY)][BTN_RIGHT] = {
    #        'type' : (0, EV_KEY),
    #        'code' : BTN_RIGHT,
    #        'value' : lambda x: 0
            # if x==0 else 1
    #}
