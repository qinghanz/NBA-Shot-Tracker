from draw import get_player_shotchartdetail, shot_chart, plt

if __name__ == "__main__":

    player_name = "Jeremy Lin"
    season_id = "2011-12"

    # Get Shotchart Data using nba_api
    player_shotchart_df, league_avg = get_player_shotchartdetail(player_name, season_id)

    # chart title
    title = player_name + " " + season_id + " Shot Chart "

    # Draw Court and plot Shot Chart
    shot_chart(player_shotchart_df, title=title)

    # Set the size for our plots
    plt.rcParams["figure.figsize"] = (15, 15)
    plt.show()
