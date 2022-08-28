from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc


def draw_court(ax=None, color="black", lw=0.9, outer_lines=False):

    if ax is None:
        ax = plt.gca()

    hoop = Circle((0, 0), radius=10, linewidth=lw, color="black", fill=False)
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color="black")

    # The paint
    outer_box = Rectangle(
        (-80, -47.5), 160, 190, linewidth=lw, color="black", fill=False
    )
    inner_box = Rectangle(
        (-60, -47.5), 120, 190, linewidth=lw, color="black", fill=False
    )

    # Top Arc
    top_free_throw = Arc(
        (0, 142.5),
        120,
        120,
        theta1=0,
        theta2=180,
        linewidth=lw,
        color="black",
        fill=False,
    )

    # Bottom Arc
    bottom_free_throw = Arc(
        (0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color="black"
    )

    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color="black")

    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color="black")
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color="black")
    three_arc = Arc(
        (0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color="black"
    )

    # Center Court
    center_outer_arc = Arc(
        (0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color="black"
    )

    # list of court shapes
    court_elements = [
        hoop,
        backboard,
        outer_box,
        inner_box,
        top_free_throw,
        bottom_free_throw,
        restricted,
        corner_three_a,
        corner_three_b,
        three_arc,
        center_outer_arc,
    ]

    if outer_lines:
        outer_lines = Rectangle(
            (-250, -47.5), 500, 470, linewidth=lw, color="black", fill=False
        )
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)


# Shot Chart Function
def shot_chart(
    data,
    title="",
    color="b",
    xlim=(-250, 250),
    ylim=(422.5, -47.5),
    line_color="black",
    court_color="white",
    court_lw=2,
    outer_lines=False,
    flip_court=False,
    gridsize=None,
    ax=None,
    despine=False,
):

    if ax is None:
        ax = plt.gca()

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    # draws the court using the draw_court method that we previously made
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # separate make or miss
    x_missed = data[data["EVENT_TYPE"] == "Missed Shot"]["LOC_X"]
    y_missed = data[data["EVENT_TYPE"] == "Missed Shot"]["LOC_Y"]

    x_made = data[data["EVENT_TYPE"] == "Made Shot"]["LOC_X"]
    y_made = data[data["EVENT_TYPE"] == "Made Shot"]["LOC_Y"]

    # place missed shots
    ax.scatter(x_missed, y_missed, c="r", marker="x", s=30, linewidths=1.25)
    # place made shots
    ax.scatter(
        x_made,
        y_made,
        facecolors="none",
        edgecolors="g",
        marker="o",
        s=30,
        linewidths=1.25,
    )

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhat unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax


# function that gets player shot detail of a specific NBA player according to specific season
def get_player_shotchartdetail(player_name, season_id):

    # getting the player from dictionary of all players
    nba_players = players.get_players()
    player_dict = [
        player for player in nba_players if player["full_name"] == player_name
    ][0]

    # career stats of specific player
    career = playercareerstats.PlayerCareerStats(player_id=player_dict["id"])
    career_df = career.get_data_frames()[0]

    # team id according to the specific season
    team_id = career_df[career_df["SEASON_ID"] == season_id]["TEAM_ID"]

    # shotchartdetail endpoints
    shotchartlist = shotchartdetail.ShotChartDetail(
        team_id=int(team_id),
        player_id=int(player_dict["id"]),
        season_type_all_star="Regular Season",
        season_nullable=season_id,
        context_measure_simple="FGA",
    ).get_data_frames()

    return shotchartlist[0], shotchartlist[1]
