import webbrowser
import os
import re
import media

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Entertainment</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet"
    href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet"
    href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src=
    "http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src=
    "https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <link href=
    "https://fonts.googleapis.com/css?family=Special+Elite" rel="stylesheet">
    <link href=
    "https://fonts.googleapis.com/css?family=Frijole" rel="stylesheet">
    <style type="text/css" media="screen">
        * {
            box-sizing: border-box;
        }
        body {
            padding-top: 80px;
            background-color: #F0FFFF;
            color: #000000;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        #dropdown1{
            display: inline-block;
        }
        #dropdown2{
            display: inline-block;
        }
        #rating{
            color: #8B0000;
            font-family: 'Special Elite', cursive;
        }
        #MovieDB{
            height: 50px;
        }
        h2, .h2{
            font-size: 20px;
        }
        .col-md-6, col-lg-4{
            width: 380px;
            height: 463px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #6495ED;
            cursor: pointer;
        }
        .navbar-inverse {
            background-image:
              linear-gradient(to bottom,#417ff0 0,#cfdef3  100%);
        }
        .navbar-inverse .navbar-brand {
            color: #191970;
            font-size: 36px;
            font-family: 'Frijole', cursive;
        }
        .navbar {
            border: none;
        }
        .navbar-inverse .navbar-brand:hover,
        .navbar-inverse .navbar-brand:focus {
            color: black;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, \
        .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself
            // gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = \
            $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' \
            + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty(). \
            append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" \
          aria-hidden="true">
            <img src= \
            "https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-header">
            <img id="MovieDB" src= \
            "https://www.themoviedb.org/assets/static_cache/41bdcf10bbf6f84c0fc73f27b2180b95/images/v4/logos/91x81.png"
            alt="MovieDB"><a class="navbar-brand">Latest Movies</a>
          </div>
      </nav>
      </div>
    <div class="container">
      {tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" \
  data-trailer-youtube-id="{trailer_youtube_id}" \
  data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2 class="header">{title} <span id="rating">{rating}<span></h2>
    <div id="dropdown1">
      <button class="btn-group dropdown" type="button" \
      id="dropdownMenu2" data-toggle="dropdown" \
      aria-haspopup="true" aria-expanded="false">
          Additional Info
      <span class="caret"></span>
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenu2">
        <li>{duration}</li>
      </ul>
    </div>
    <div id="dropdown2">
      <button class="btn btn-default dropdown-toggle" type="button" \
        id="dropdownMenu1" data-toggle="dropdown" \
        aria-haspopup="true" aria-expanded="false">
          Story Line
      <span class="caret"></span>
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
        <li>{storyline}</li>
      </ul>
    </div>
</div>

'''


def create_tiles_content(entertainment):
    # The HTML content for this section of the page
    content = ''
    for distraction in entertainment:
        # Extract the youtube ID from the url
        youtube_id_match = \
        re.search(r'(?<=v=)[^&#]+', distraction.trailer_youtube_url)
        youtube_id_match = \
        youtube_id_match \
        or re.search(r'(?<=be/)[^&#]+', distraction.trailer_youtube_url)
        trailer_youtube_id = \
        youtube_id_match.group(0) if youtube_id_match else None
        # this part checks to see if the distraction is part of the class
        # Movie or Tv_show class and then allows the additional info to
        # be into the template
        if isinstance(distraction, media.Movie):
            rating_match = distraction.rating
        else:
            rating_match = ""

        if isinstance(distraction, media.Movie):
            additional_duration = "Total Duration: " + distraction.duration
        else:
            additional_duration = ""

        # Append the tile for the movie with its content filled in
        content += tile_content.format(
            title=distraction.title,
            storyline=distraction.storyline,
            poster_image_url=distraction.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            rating=rating_match,
            duration=additional_duration)

    return content


def open_movies_page(entertainment):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')
    # Replace the placeholder for the movie
    # tiles with the actual dynamically generated content
    rendered_content = main_page_content. \
    format(tiles=create_tiles_content(entertainment))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)  # open in a new tab, if possible
