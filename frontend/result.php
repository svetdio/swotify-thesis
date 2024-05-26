<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SA Result</title>
    <link rel="icon" href="assets/sentiment-analysis.png">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/versions/bulma-no-dark-mode.min.css">
</head>

<body>
    <div class="container is-fluid">
        <section class="hero is-primary">
            <div class="hero-body is-flex is-justify-content-space-between">
                <p class="title">Model Validation Results</p>
                <a href="testform.php" onclick="history.go(-1);">
                    <input class="button" type="submit" name="Submit" value="Back" style="font-weight: bold;">
                </a>
            </div>
        </section>

        <div class="grid">
            <div class="cell has-background-light has-text-success-invert has-radius-normal p-3 mt-2 has-text-centered ">
                <div class="label is-size-5">K-NEAREST NEIGHBORS</div>
                <div class="label">Predicted Sentiment: </div>
                <div class="result">
                    <div id="knn" class='is-size-4 has-text-weight-bold'></div>
                </div>
            </div>
            <div class="cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                <div class="label is-size-5">SUPPORT VECTOR MACHINE</div>
                <div class="label">Predicted Sentiment: </div>
                <div class="result">
                    <div id="svc" class='is-size-4 has-text-weight-bold'></div>
                </div>
            </div>
            <div class="cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                <div class="label is-size-5">GRADIENT BOOSTING</div>
                <div class="label">Predicted Sentiment: </div>
                <div class="result">
                    <div id="xgb" class='is-size-4 has-text-weight-bold'></div>
                </div>
            </div>
        </div>


        <section class="hero py-3 px-4 has-background-primary-light has-radius-normal">
            <div class="hero-body">
                <div class="fixed-grid has-3-cols">
                    <div class="grid">
                        <div class="cell is-size-5 has-text-weight-bold">Actual Sentiment: </div>
                        <div class="cell is-col-span-2 is-size-5 has-text-weight-bold" id="actual_pred"></div>
                    </div>
                </div>
            </div>
        </section>


        <div class="grid">
            <div class="cell mt-2">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Questions</th>
                            <th>Response</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>He/She was well-prepared for his/her responsibilities during the Local CAF 2024?</td>
                            <td><?php echo $_POST['responsibility_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She effectively communicated with his/her team members before and during the Local CAF 2024?</td>
                            <td><?php echo $_POST['team_communication_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She was able to delegate tasks effectively and ensure he/she were completed on time?</td>
                            <td><?php echo $_POST['task_delegation_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She remained calm and collected under pressure during the event?</td>
                            <td><?php echo $_POST['calmness_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She was able to adapt to unexpected challenges and changes before or during the Local CAF 2024?</td>
                            <td><?php echo $_POST['adaptability_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She consistently displayed a positive and enthusiastic attitude throughout the Local CAF 2024?</td>
                            <td><?php echo $_POST['attitude_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>Do you think he/she face any difficulties with communication or collaboration during the event?</td>
                            <td><?php echo $_POST['comm_collab_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>In any external factors that threatened the success of the event, did he/she respond relatively?</td>
                            <td><?php echo $_POST['external_resp_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She did not effectively manage his/her time during the event?</td>
                            <td><?php echo $_POST['time_management_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She did not collaborate effectively with other CSG officers or committees?</td>
                            <td><?php echo $_POST['collab_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She was not flexible in his/her approach to problem-solving during the Local CAF 2024?</td>
                            <td><?php echo $_POST['flexible_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>He/She did not take responsibility for his/her mistakes or the mistakes of his/her team?</td>
                            <td><?php echo $_POST['accountability_rating'] ?></td>
                        </tr>
                        <tr>
                            <td>What do you think is his/her greatest contribution and what opportunity did he/she unlock during Local CAF 2024 event?</td>
                            <td><?php echo $_POST['event_contribution'] ?></td>
                        </tr>
                        <tr>
                            <td>Do you have any comment, suggestion/s, and recommendation/s?</td>
                            <td><?php echo $_POST['comment_feedback'] ?></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        let data = JSON.parse(JSON.stringify(<?php echo json_encode($_POST); ?>))
        fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "responsibility_rating": data.responsibility_rating,
                    "team_communication_rating": data.team_communication_rating,
                    "task_delegation_rating": data.task_delegation_rating,
                    "calmness_rating": data.calmness_rating,
                    "adaptability_rating": data.adaptability_rating,
                    "attitude_rating": data.attitude_rating,
                    "comm_collab_rating": data.comm_collab_rating,
                    "external_resp_rating": data.external_resp_rating,
                    "time_management_rating": data.time_management_rating,
                    "collab_rating": data.collab_rating,
                    "flexible_rating": data.flexible_rating,
                    "accountability_rating": data.accountability_rating,
                    "event_contribution": data.event_contribution,
                    "comment_feedback": data.comment_feedback,
                }),
            })
            .then(response => response.json())
            .then(data => {
                let knn_pred = 'Positive';
                let svc_pred = 'Positive';
                let xgb_pred = 'Positive';

                let knn_class = "has-text-success";
                let svc_class = "has-text-success";
                let xgb_class = "has-text-success";

                let actual_sent = "has-text-success"

                if (data.knn_prediction == 0) {
                    knn_pred = 'Neutral'
                    knn_class = 'has-text-link-light'
                } else if (data.knn_prediction > 1) {
                    knn_pred = 'Negative'
                    knn_class = 'has-text-danger'
                }

                if (data.svc_prediction == 0) {
                    svc_pred = 'Neutral'
                    svc_class = 'has-text-link-light'
                } else if (data.svc_prediction > 1) {
                    svc_pred = 'Negative'
                    svc_class = 'has-text-danger'
                }

                if (data.xgb_prediction == 0) {
                    xgb_pred = 'Neutral'
                    xgb_class = 'has-text-link-light'
                } else if (data.xgb_prediction > 1) {
                    xgb_pred = 'Negative'
                    xgb_class = 'has-text-danger'
                }


                if (data.sentiment_class == "NEUTRAL") {
                    actual_sent = 'has-text-link-light'
                } else if (data.sentiment_class == "NEGATIVE") {
                    actual_sent = 'has-text-danger'
                }

                document.getElementById('knn').textContent = knn_pred;
                document.getElementById('knn').classList.add(knn_class);

                document.getElementById('svc').textContent = svc_pred;
                document.getElementById('svc').classList.add(svc_class);

                document.getElementById('xgb').textContent = xgb_pred;
                document.getElementById('xgb').classList.add(xgb_class);
                
                document.getElementById('actual_pred').textContent = data.sentiment_class
                document.getElementById('actual_pred').classList.add(actual_sent);

            })
    </script>
</body>

</html>