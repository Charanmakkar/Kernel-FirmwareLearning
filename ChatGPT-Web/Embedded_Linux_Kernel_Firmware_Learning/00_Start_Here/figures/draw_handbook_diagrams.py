"""Original teaching diagrams. Run with the primary runtime Python and matplotlib."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib.path import Path as MPath

OUT=Path(__file__).resolve().parent
NAVY='#182D45'
EDGE='#26384A'
LIGHT='#F3F5F7'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.unicode_minus':False})

def canvas(height,title,subtitle=None):
    fig,ax=plt.subplots(figsize=(6.8,height),dpi=220)
    fig.patch.set_facecolor('white')
    ax.set_position([.02,.02,.96,.96]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    ax.text(.5,.98,title,ha='center',va='top',fontsize=15,fontweight='bold',color=NAVY)
    if subtitle:ax.text(.5,.944,subtitle,ha='center',va='top',fontsize=9.5,color=EDGE)
    return fig,ax

def box(ax,cx,cy,w,h,head,body='',fs=10.6,fill='white',headfs=11.2):
    rect=FancyBboxPatch((cx-w/2,cy-h/2),w,h,boxstyle='round,pad=0.008,rounding_size=0.008',facecolor=fill,edgecolor=EDGE,linewidth=1.15)
    ax.add_patch(rect)
    if body:
        ax.text(cx,cy+h/2-.016,head,ha='center',va='top',fontsize=headfs,fontweight='bold',color=NAVY,linespacing=1.15)
        ax.text(cx,cy-.014,body,ha='center',va='center',fontsize=fs,color='#111111',linespacing=1.35)
    else:ax.text(cx,cy,head,ha='center',va='center',fontsize=headfs,fontweight='bold',color=NAVY,linespacing=1.3)
    return (cx-w/2,cy-h/2,cx+w/2,cy+h/2)

def arrow(ax,pts,label=None,labelxy=None,dashed=False):
    verts=pts
    path=MPath(verts,[MPath.MOVETO]+[MPath.LINETO]*(len(verts)-1))
    patch=FancyArrowPatch(path=path,arrowstyle='-|>',mutation_scale=10,linewidth=1.2,color=EDGE,linestyle='--' if dashed else '-')
    ax.add_patch(patch)
    if label:
        x,y=labelxy or ((pts[0][0]+pts[-1][0])/2,(pts[0][1]+pts[-1][1])/2)
        ax.text(x,y,label,ha='center',va='center',fontsize=9,color=EDGE,bbox={'facecolor':'white','edgecolor':'none','pad':1.4})

def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=220,facecolor='white')
    fig.savefig(OUT/(name+'.svg'),facecolor='white')
    plt.close(fig)

# 1. Prerequisites: a teaching sequence, not a claim that every JD needs every module.
fig,ax=canvas(8.1,'Learning prerequisites','Progress by demonstrated exits; revisit failed prerequisites before advancing')
box(ax,.5,.835,.86,.15,'Shared foundations',
    'M01  Environment, tools and Git\nM02  C ownership and undefined behavior\nM03  Data structures and defensive parsing\nM04  Compilation, linking and relevant C++',fill=LIGHT)
box(ax,.5,.635,.86,.13,'Systems foundations',
    'M05  Operating systems and architecture\nM06  POSIX I/O and processes\nM07  Concurrency and IPC',fill=LIGHT)
arrow(ax,[(.5,.752),(.5,.708)])
box(ax,.255,.427,.405,.18,'Linux and kernel branch',
    'M08  Cross tools, boot and device tree\nM09  Kernel contexts and lifetimes\nM10  Character and platform drivers\nM11  Buses, IIO, DMA and power\nM14  Buildroot and Yocto images',fs=9.9,headfs=10.8)
box(ax,.745,.427,.405,.18,'MCU and firmware branch',
    'M12  Startup, memory and peripherals\nM13  RTOS and Linux MCU protocol\n\nFirst validate in a simulator;\nthen build and measure on a board',fs=9.9,headfs=10.8)
arrow(ax,[(.5,.562),(.5,.54),(.255,.54),(.255,.525)])
arrow(ax,[(.5,.54),(.745,.54),(.745,.525)])
box(ax,.5,.254,.86,.10,'Integration and evidence',
    'M15  Debugging and performance   •   M17  Integration and tests',fs=10.0,fill=LIGHT)
arrow(ax,[(.255,.329),(.255,.316),(.5,.316),(.5,.312)])
arrow(ax,[(.745,.329),(.745,.316),(.5,.316)])
box(ax,.5,.105,.86,.115,'Production practice and capstones',
    'M16  Updates, security and reliability   •   M18  Responsible AI\nC01  Monitoring gateway   •   C02  Robot control demonstrator',fs=10.0)
arrow(ax,[(.5,.196),(.5,.171)])
ax.text(.5,.018,'Branches are related career tracks. Depth follows the target JD and assessment evidence.',ha='center',va='center',fontsize=9,color=EDGE)
save(fig,'01_prerequisite_map')

# 2. The delivered code runs in one host process; the boundaries are architectural.
fig,ax=canvas(8.0,'Linux and MCU responsibilities','C02 evidence: deterministic host simulation; no physical motor outputs')
box(ax,.59,.815,.69,.145,'Linux role',
    'Plan motion and publish bounded wheel commands\nRefresh commands every 50 ms in the lab scenario\nCollect diagnostics and explain faults',fill=LIGHT,fs=10.3)
box(ax,.59,.615,.69,.13,'Protocol boundary',
    'Version, sequence, wheel setpoints and CRC\nReject malformed or out of range messages\nCRC detects corruption; it does not authenticate',fs=10.0)
arrow(ax,[(.59,.734),(.59,.688)],label='command frame',labelxy=(.71,.712))
box(ax,.59,.385,.69,.21,'MCU role',
    'Validate frame, sequence and local speed limits\nRefresh freshness only after a valid new command\nExpire demand at 200 ms; output becomes zero\nLatch a local stop until deliberate rearm\nRearm alone does not request motion',fill=LIGHT,fs=10.0)
arrow(ax,[(.59,.542),(.59,.498)])
box(ax,.115,.385,.18,.18,'Local stop',
    'Separate from\nLinux commands\n\nSoftware latch\nin this model',fs=9.3,headfs=10.3)
arrow(ax,[(.213,.385),(.237,.385)])
box(ax,.59,.167,.69,.125,'Actuator and feedback simulation',
    'Differential drive integrated at 10 ms steps\nRecord wheel output, pose and controller state',fs=10.0)
arrow(ax,[(.59,.272),(.59,.238)],label='limited output',labelxy=(.73,.255))
arrow(ax,[(.943,.167),(.972,.167),(.972,.815),(.943,.815)],dashed=True)
ax.text(.993,.49,'diagnostic feedback only',ha='center',va='center',rotation=90,fontsize=8.7,color=EDGE,bbox={'facecolor':'white','edgecolor':'none','pad':1})
ax.text(.5,.04,'The stop path is modeled software. Real MCU timing, motor dynamics and an independent\nhardware stopping circuit require separate design and validation.',ha='center',va='center',fontsize=9.0,color=EDGE,linespacing=1.3)
save(fig,'02_linux_mcu_boundary')

# 3. Authenticated-before-write and reverified-after-write agree with update.py.
fig,ax=canvas(9.1,'Signed A B update lifecycle','A03 evidence: host file slots and simulated boot selection')
box(ax,.5,.86,.73,.078,'Known good A remains active',fill=LIGHT)
box(ax,.5,.74,.73,.09,'Authenticate release bundle',
    'Signature, compatibility, version and payload digest',fs=10.0)
arrow(ax,[(.5,.813),(.5,.793)])
box(ax,.5,.609,.73,.105,'Stage inactive B',
    'Write verified bytes and fsync\nReverify the slot; commit pending B and attempts 0',fs=10.0)
arrow(ax,[(.5,.687),(.5,.67)])
# Reject path leaves known-good state unchanged.
arrow(ax,[(.127,.74),(.07,.74),(.07,.86),(.127,.86)],label='reject',labelxy=(.073,.80))
box(ax,.5,.463,.73,.11,'Trial boot B',
    'Persist an attempt before selecting the candidate\nAt most two unconfirmed trials',fs=10.0,fill=LIGHT)
arrow(ax,[(.5,.549),(.5,.526)])
# Decision diamond.
cy=.322;wx=.155;hy=.053
ax.add_patch(Polygon([[.5,cy+hy],[.5+wx,cy],[.5,cy-hy],[.5-wx,cy]],closed=True,facecolor='white',edgecolor=EDGE,linewidth=1.15))
ax.text(.5,cy,'Health\nconfirmed?',ha='center',va='center',fontsize=10.5,fontweight='bold',color=NAVY,linespacing=1.2)
arrow(ax,[(.5,.40),(.5,.383)])
box(ax,.245,.171,.405,.125,'Commit B',
    'B becomes known good\nAdvance minimum accepted version\nClear pending state and attempt count',fs=9.6,headfs=10.7)
box(ax,.755,.171,.405,.125,'Leave unconfirmed',
    'Next boot retries while budget remains\nExhausted budget restores A\nCorrupt trial image falls back to A',fs=9.6,headfs=10.7)
arrow(ax,[(.337,.322),(.245,.322),(.245,.242)],label='yes',labelxy=(.285,.324))
arrow(ax,[(.663,.322),(.755,.322),(.755,.242)],label='no',labelxy=(.718,.324))
# Retry loop routed outside the main flow; no automatic unlimited retries.
arrow(ax,[(.965,.171),(.984,.171),(.984,.463),(.873,.463)],dashed=True)
ax.text(.983,.318,'retry only with budget',ha='center',va='center',rotation=90,fontsize=8.3,color=EDGE,bbox={'facecolor':'white','edgecolor':'none','pad':1})
ax.text(.5,.046,'This does not establish secure boot or tamper resistant rollback state.\nReal bootloader integration, flash power cut tests and trust anchor protection remain pending.',ha='center',va='center',fontsize=9.0,color=EDGE,linespacing=1.3)
save(fig,'03_signed_ab_lifecycle')
