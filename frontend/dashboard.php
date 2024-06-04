<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SWOTify Sentiment Analysis</title>
    <link rel="icon" href="assets/sentiment-analysis.png">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/versions/bulma-no-dark-mode.min.css">
    <link rel="stylesheet" href="https://bulma.io/vendor/fontawesome-free-6.5.2-web/css/all.min.css">
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.13.3/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/2.0.8/css/dataTables.dataTables.css" />
    <link rel="stylesheet" href="dashboard/dashboard.css">
</head>

<body>
    <nav class="navbar is-link" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="index.php">
                <img src="assets/sentiment-analysis.png" alt="Page logo">
            </a>

            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>

        <div id="navbarBasicExample" class="navbar-menu">
            <div class="navbar-start">
                <a href="index.php" class="navbar-item">Home</a>
                <a href="dashboard.php" class="navbar-item is-selected">Analysis Dashboard</a>
                <a href="form.php" class="navbar-item">Model Validation Form</a>
            </div>
        </div>

        <div class="navbar-end">
            <div class="navbar-item">
                <a href="https://colab.research.google.com/drive/1nGLgxrAnrBgf3PYlc9shmnaHIEH_ywDi#scrollTo=zUSzysEZHOMy" class="navbar-item">Training Notebook</a>
            </div>
        </div>
    </nav>

    <section class="hero is-small is-primary">
        <div class="hero-body">
            <p class="subtitle has-text-weight-semibold">Analysis Dashboard</p>
        </div>
    </section>

    <section class="section p-2">
        <div class="container is-fluid">
            <div class="columns">
                <div class="column is-3">
                    <div class="box m-1">
                        <p class="title is-5">CSG Officers List</p>
                        <div class="field">
                            <label class="label">Full Name</label>
                            <div class="control has-icons-left has-icons-right">
                                <input class="input" type="text" id="csg-officers" placeholder="Enter name">
                                <span class="icon is-small is-left">
                                    <i class="fas fa-user"></i>
                                </span>
                            </div>
                        </div>

                        <div class="field">
                            <p class="control">
                                <button id="sa_evaluate" class="button is-primary is-fullwidth">
                                    View Result
                                </button>
                            </p>
                        </div>
                    </div>
                </div>

                <div id="loading-screen" class="column">
                    <div class="columns">
                        <div class="column">
                            <div class="box">
                                <p class="subtitle">
                                    Enter the name of the CSG officer, then click "View Results" button.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="results-pane" class="column is-hidden">
                    <div class="columns">
                        <div class="column">
                            <div class="box m-1">
                                <p class="subtitle">
                                    Total Evaluations Received
                                </p>
                                <p id="total_eval_received" class="main_score title is-4">123</p>
                            </div>
                        </div>

                        <div class="column">
                            <div class="box m-1">
                                <p class="subtitle">
                                    Positive Reviews
                                </p>
                                <p id="positive_sentiment" class="main_score title is-4">123</p>
                            </div>
                        </div>
                        <div class="column">
                            <div class="box m-1">
                                <p class="subtitle">
                                    Neutral Reviews
                                </p>
                                <p id="neutral_sentiment" class="main_score title is-4">123</p>
                            </div>
                        </div>
                        <div class="column">
                            <div class="box m-1">
                                <p class="subtitle">
                                    Negative Reviews
                                </p>
                                <p id="negative_sentiment" class="main_score title is-4">123</p>
                            </div>
                        </div>
                    </div>

                    <div class="columns">
                        <div class="column is-one-quarter">
                            <div class="box m-1">
                                <p class="title is-5">Sentiment Distribution</p>
                                <p class="subtitle is-7">
                                    Generated by the ML Model
                                </p>

                                <canvas id="sentiment_distribution"></canvas>
                            </div>
                        </div>
                        <div class="column">
                            <div class="box m-1">
                                <p class="title is-5">Performance Ratings</p>
                                <p class="subtitle is-7">
                                    Averaged Performance Ratings
                                </p>
                                <div id="legend-container"></div>
                                <canvas id="performance_ratings"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="columns">
                        <div class="column">
                            <div class="box m-1">
                                <p class="title is-5">All Feedback</p>
                                <table id="sentiment_comments" class="table is-hoverable is-striped is-narrow" style="width: 100%">
                                    <thead>
                                        <tr>
                                            <!-- <th>Evaluator</th> -->
                                            <th>Event Contribution</th>
                                            <th>Comment and Feedback</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


        </div>
    </section>


    <script src="https://code.jquery.com/jquery-3.7.1.js"></script>
    <script src="https://code.jquery.com/ui/1.13.3/jquery-ui.js"></script>
    <script src="https://cdn.datatables.net/2.0.8/js/dataTables.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@latest/dist/chartjs-plugin-datalabels.min.js"></script>
    <script src="dashboard/dashboard.js"></script>

</body>

</html>