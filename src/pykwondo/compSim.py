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
    for axis in ax.values(): 
        axis.clear()

    plt.suptitle(f"Pykwondo! - Timestep #{comp.get_timestep()}")

# Arena axis
    axis = ax["arena"]
    axis.imshow(floor, cmap='Pastel1', vmin=0, vmax=1)
    axis.set_title("Competition Grounds!")
    
    # Iterate through clubs
    for club in comp.get_clubs():
        i = comp.get_clubs().index(club)
        # Club name labels
        axis.annotate(f"{club.get_name()}", xy=(1,1+10*i))
        
        # Draw competitors
        for competitor in club.get_competitors():
            pos = competitor.get_pos()
            axis.scatter(pos[0], pos[1]+5+10*i, 
                          color=competitor.get_rank())

    # Arena event type label
    axis.annotate(f"Event", xy=(21,1))
    
# Team score graph
    axis = ax["club_scores"]
    axis.set_title("Club scores!")
    axis.set_xlabel('Points')
    axis.set_ylabel('Club')

    clubs = sorted(comp.get_clubs(), key=lambda club: club.get_score())
    # Map team colours for bar graph to match the team areas
    cmap = plt.get_cmap('Pastel1')
    colors = [cmap(comp.get_clubs().index(club)) for club in clubs]
    # Draw bar graph
    axis.barh([club.get_name() for club in clubs],
                          [club.get_score() for club in clubs],
                          color=colors)

# Individual score graph
    axis = ax['individual_scores']

    clubs = comp.get_clubs()
    axis.set_ylim(-0.5, 3.5)
    axis.set_yticks(range(len(clubs)),
                    (club.get_name() for club in clubs))
    for club in clubs:
        for competitor in club.get_competitors():
            # Competitor parameters
            name, score, i = competitor.get_name(), competitor.get_score(), clubs.index(club)

            axis.scatter(score, i, color=competitor.get_rank())
            axis.annotate(f'{name}: {score}', xy=(score, i))

    # Pause the plot
    plt.pause(2)

comp = Comp()
# Initialise figure and axis, mosaic subplot allows 1 plot on the left
# and 2 plots on the right.
#fig, ax = plt.subplot_mosaic([["arena","club_scores","individual_scores"],
#                              ["arena","bro","individual_scores"]],
#                             figsize=(19.2, 10.8),
#                             width_ratios=[5,2,2],
#                             gridspec_kw={"hspace": 0.3, "wspace": 0.3})

fig = plt.figure(figsize=(19.2, 10.8), layout="constrained")
gs = fig.add_gridspec(2,3) # 2 rows 3 columns
ax = {
    "arena":                fig.add_subplot(gs[:, 0]), 
    "club_scores":          fig.add_subplot(gs[0, 1]), 
    "extra":                fig.add_subplot(gs[1, 1]),
    "individual_scores":    fig.add_subplot(gs[:, 2])
    }

plt.rcParams.update({'axes.labelsize': 14, 'xtick.labelsize': 12,
                     'ytick.labelsize': 8})

zeros_arr = np.zeros((40, 60))
floor = init_background(zeros_arr)

comp.create_schedule()
draw()
