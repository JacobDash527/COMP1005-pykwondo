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
    axis.set_adjustable("datalim")
    axis.imshow(floor, cmap='Pastel1', vmin=0, vmax=1)
    axis.set_title("Competition Grounds!")
    
    # Iterate through clubs
    for club in comp.get_clubs():
        i = comp.get_clubs().index(club)
        # Club name labels
        axis.annotate(f"{club.get_name()}", xy=(1,1+10*i))
        
        # Draw competitors
        for competitor in club.get_competitors():
            j = club.get_competitors().index(competitor)
            pos = competitor.get_pos()
            axis.scatter(pos[0]+j*1.5, pos[1]+5+10*i, 
                          color=competitor.get_rank())

    # Arena event type label
    axis.annotate(f"Event", xy=(21,1))
    
# Team score graph
    axis = ax["club_scores"]
    axis.set_title("Club scores!")
    axis.set_xlabel('Points')

    clubs = sorted(comp.get_clubs(), key=lambda club: club.get_score())
    # Map team colours for bar graph to match the team areas
    cmap = plt.get_cmap('Pastel1')
    colors = [cmap(comp.get_clubs().index(club)) for club in clubs]
    # Draw bar graph
    axis.barh([club.get_name() for club in clubs],
                          [club.get_score() for club in clubs],
                          color=colors)

# Individual score table
    axis = ax['individual_scores']
    axis.set_title("Individual scores!")
    axis.set_xticks([])
    axis.set_yticks([])
    
    # List of competitors sorted by score
    competitors = sorted(comp.combine_competitors(), 
                         key=lambda competitor: competitor.get_score())
    rows = range(1, len(competitors))
    columns = ['Rank', 'Name', 'Club', 'Score', 'Belt']
    cell_text = [[i+1, competitor.get_name().replace(" ","\n"), 
                  competitor.get_club_name().replace(" ","\n"), 
                  competitor.get_score(), 
                  competitor.get_rank().capitalize()] 
                 for i, competitor in enumerate(competitors)]
    
    table = axis.table(cellText=cell_text, colLabels=columns, 
                       bbox=[0,0,1,1])
    table.auto_set_font_size(False)
    table.set_fontsize(6)

    # Pause the plot
    plt.pause(5)

comp = Comp()
# Initialise figure and axis, mosaic subplot allows 1 plot on the left
# and 2 plots on the right.
#fig, ax = plt.subplot_mosaic([["arena","club_scores","individual_scores"],
#                              ["arena","bro","individual_scores"]],
#                             figsize=(19.2, 10.8),
#                             width_ratios=[5,2,2],
#                             gridspec_kw={"hspace": 0.3, "wspace": 0.3})

fig = plt.figure(figsize=(14, 10), layout="constrained")
gs = fig.add_gridspec(2, 3, width_ratios=[2,1,1]) # 2 rows 3 columns
ax = {
    "arena":                fig.add_subplot(gs[:, 0]), 
    "club_scores":          fig.add_subplot(gs[0, 1]), 
    "extra":                fig.add_subplot(gs[1, 1]),
    "individual_scores":    fig.add_subplot(gs[:, 2])
    }

plt.rcParams.update({'axes.labelsize': 10, 'xtick.labelsize': 12,
                     'ytick.labelsize': 8})

zeros_arr = np.zeros((40, 60))
floor = init_background(zeros_arr)

comp.create_schedule()
draw()
