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

    <section class="hero is-fullheight is-primary">
        <div class="hero-head">
            <nav class="navbar" role="navigation" aria-label="main navigation">
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
                        <a href="index.php" class="navbar-item is-selected">Home</a>
                        <a href="dashboard.php" class="navbar-item">Analysis Dashboard</a>
                        <a href="form.php" class="navbar-item">Model Validation Form</a>
                    </div>
                </div>

                <div class="navbar-end">
                    <div class="navbar-item">
                        <a href="https://colab.research.google.com/drive/1nGLgxrAnrBgf3PYlc9shmnaHIEH_ywDi#scrollTo=zUSzysEZHOMy" class="navbar-item">Training Notebook</a>
                    </div>
                </div>
        </div>
        </nav>
        </div>
        <div class="hero-body">
            <div class="">
                <p class="title">SWOTify Sentiment Analysis</p>
                <p class="subtitle">This study explores conducting sentiment analysis on the SWOTify platform. Using natural language processing (NLP) and machine learning, sentiment analysis categorizes text as positive, negative, or neutral and detects emotions, providing valuable insights across various sectors. The researchers developed a sentiment analysis architecture following a conceptual framework. This framework included data collection, preprocessing, exploratory data analysis, sentiment analysis and modeling, aggregation and scoring, and model validation. The sentiment analysis provided valuable insights into how officers viewed and assessed various leadership aspects. An exploration of the correlations between sentiment and leadership qualities, such as decisiveness, resource utilization, and communication style, revealed significant relationships, suggesting a significant relationship between sentiment and these leadership attributes. The dominant sentiment identified in the study was positive. Three data models were identified as suitable for the dataset. Following hyperparameter tuning and evaluation, researchers found that the K-Nearest Neighbors algorithm achieved the best fit for the SWOTify data, with an F1 score of 83%. Ultimately, after evaluation with the respondents, the researchers found the model and sentiment analysis results to be functional, efficient, reliable, usable, and well-performing.</p>
            </div>
        </div>
    </section>

</body>

</html>