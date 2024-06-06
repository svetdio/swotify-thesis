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
        <!-- <div class="navbar-brand">
            <a class="navbar-item" href="index.php">
                <img src="assets/sentiment-analysis.png" alt="Page logo">
            </a>

            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div> -->

        <div id="navbarBasicExample" class="navbar-menu">
            <div class="navbar-start">
                <a href="index.php" class="navbar-item is-selected">Home</a>
                <a href="dashboard.php" class="navbar-item">Analysis Dashboard</a>
                <a href="form.php" class="navbar-item">Model Validation Form</a>
            </div>
        </div>

        <!-- <div class="navbar-end">
            <div class="navbar-item">
                <a href="https://colab.research.google.com/drive/1nGLgxrAnrBgf3PYlc9shmnaHIEH_ywDi#scrollTo=zUSzysEZHOMy" class="navbar-item">Training Notebook</a>
            </div>
        </div> -->
    </nav>

    <section class="hero is-fullheight-with-navbar">
        <div class="hero-body" id="homepage">
            <div class="container is-fluid ">
                <div class="columns is-vcentered">
                    <div class="column is-5 is-primary">
                        <figure class="image is-1by1">
                            <img src="assets/img1.png" />
                        </figure>
                    </div>
                    <div class="column is-7">

                        <p class="title titlePage">SWOTify</p>
                        <p class="subtitle titlePage">Sentiment Analysis</p>

                    </div>
                </div>
            </div>
        </div>
    </section>

</body>

</html>