#
# compSim.py - main file for martial arts simulation
#
from pykwondo import *
import matplotlib.pyplot as plt

def init_background(arr):
    arr[:] = 1

    # Initialise each club area
    for club in comp.get_clubs():
        i = comp.get_clubs().index(club)
        arr[2+10*i:9+10*i, 1:16] = 0.1+0.1*i

    # Initialise event area
    arr[2:39, 21:59] = 0.7

    return arr

def draw():
    for axis in ax: 
        axis.clear()

    plt.suptitle(f"Pykwondo! - Timestep #{comp.get_timestep()}")

    ax[0].imshow(floor, cmap='Pastel1', vmin=0, vmax=1)
    ax[0].set_title("Competition Grounds!")
    
    # Iterate through clubs
    for club in comp.get_clubs():
        i = comp.get_clubs().index(club)
        # Club name labels
        ax[0].annotate(f"{club.get_name()}", xy=(1,1+10*i))
        
        # Draw competitors
        for competitor in club.get_competitors():
            pos = competitor.get_pos()
            ax[0].scatter(pos[0], pos[1]+5+10*i, 
                          color=competitor.get_rank())

    # Arena event type label
    ax[0].annotate(f"Event", xy=(21,1))

    plt.pause(2)

comp = Comp()
fig, ax = plt.subplots(1,2, figsize=(19.2, 10.8))
zeros_arr = np.zeros((40, 60))
floor = init_background(zeros_arr)

comp.create_schedule()
draw()
