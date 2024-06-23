<?php
$positive_rate = array(
    '5' => 'Strongly Agree',
    '4' => 'Agree',
    '3' => 'Neutral',
    '2' => 'Disagree',
    '1' => 'Strongly Disagree'
);

$negative_rate = array(
    '1' => 'Strongly Agree',
    '2' => 'Agree',
    '3' => 'Neutral',
    '4' => 'Disagree',
    '5' => 'Strongly Disagree'
);
?>

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SA Result</title>
    <link rel="icon" href="assets/sentiment-analysis.png">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/versions/bulma-no-dark-mode.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/fontawesome.min.css">
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.13.3/themes/base/jquery-ui.css">

    <link rel="stylesheet" href="dashboard/dashboard.css">

    <script src="https://code.jquery.com/jquery-3.7.1.js"></script>
    <script src="https://code.jquery.com/ui/1.13.3/jquery-ui.js"></script>
</head>

<body>
    <div class="container is-fluid">
        <section class="hero is-primary">
            <div class="hero-body is-flex is-justify-content-space-between">
                <p class="title">Model Validation Results</p>
                <a href="form.php">
                    <input class="button" type="submit" name="Submit" value="Back" style="font-weight: bold;">
                </a>
            </div>
        </section>




        <section class="hero py-3 px-4 has-background-primary-light has-radius-normal is-hidden">
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
            <div id="tabs">
                <ul>
                    <li><a href="#tabs-1">Results</a></li>
                    <li><a href="#tabs-2">Base Model</a></li>
                    <li><a href="#tabs-3">CSG Trained Models</a></li>
                    <li><a href="#tabs-4">Self-trained Models</a></li>
                </ul>
                <div id="tabs-1">
                    <div class="cell mt-2">
                        <div class="cell has-background-white-ter has-text-primary-invert has-radius-normal p-5">
                            <div class="content">
                                <p class="is-size-5"><b>Name of the Evaluatee:</b> <?php echo htmlspecialchars($_POST['evaluatee']); ?></p>
                                <p class="is-size-5"><b>Position of the Evaluatee:</b> <?php echo htmlspecialchars($_POST['position']); ?></p>
                            </div>
                        </div>

                        <table id="modelResult" class="table is-fullwidth">
                            <tbody>
                                <tr>
                                    <th>Questions</th>
                                    <th>Response</th>
                                </tr>
                                <tr>
                                    <td>He/She was well-prepared for his/her responsibilities during the Local CAF 2024?</td>
                                    <td><?php echo $positive_rate[$_POST['responsibility_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She effectively communicated with his/her team members before and during the Local CAF 2024?</td>
                                    <td><?php echo $positive_rate[$_POST['team_communication_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She was able to delegate tasks effectively and ensure he/she were completed on time?</td>
                                    <td><?php echo $positive_rate[$_POST['task_delegation_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She remained calm and collected under pressure during the event?</td>
                                    <td><?php echo $positive_rate[$_POST['calmness_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She was able to adapt to unexpected challenges and changes before or during the Local CAF 2024?</td>
                                    <td><?php echo $positive_rate[$_POST['adaptability_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She consistently displayed a positive and enthusiastic attitude throughout the Local CAF 2024?</td>
                                    <td><?php echo $positive_rate[$_POST['attitude_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>Do you think he/she face any difficulties with communication or collaboration during the event?</td>
                                    <td><?php echo $negative_rate[$_POST['comm_collab_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>In any external factors that threatened the success of the event, did he/she respond relatively?</td>
                                    <td><?php echo $positive_rate[$_POST['external_resp_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She did not effectively manage his/her time during the event?</td>
                                    <td><?php echo $negative_rate[$_POST['time_management_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She did not collaborate effectively with other CSG officers or committees?</td>
                                    <td><?php echo $negative_rate[$_POST['collab_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She was not flexible in his/her approach to problem-solving during the Local CAF 2024?</td>
                                    <td><?php echo $negative_rate[$_POST['flexible_rating']] ?></td>
                                </tr>
                                <tr>
                                    <td>He/She did not take responsibility for his/her mistakes or the mistakes of his/her team?</td>
                                    <td><?php echo $negative_rate[$_POST['accountability_rating']] ?></td>
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
                <div id="tabs-2">
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
                        <div class="cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                            <div class="label is-size-5">RANDOM FOREST</div>
                            <div class="label">Predicted Sentiment: </div>
                            <div class="result">
                                <div id="rfc" class='is-size-4 has-text-weight-bold'></div>
                            </div>
                        </div>
                        <div class="cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                            <div class="label is-size-5">LOGISTIC REGRESSION</div>
                            <div class="label">Predicted Sentiment: </div>
                            <div class="result">
                                <div id="lr" class='is-size-4 has-text-weight-bold'></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="tabs-3">
                    <div class="grid">
                        <div class="cell has-background-light has-text-success-invert has-radius-normal p-3 mt-2 has-text-centered ">
                            <div class="label is-size-5">K-NEAREST NEIGHBORS</div>
                            <div class="label">Predicted Sentiment: </div>
                            <div class="result">
                                <div id="csg_knn" class='is-size-4 has-text-weight-bold'></div>
                            </div>
                        </div>
                        <div class="cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                            <div class="label is-size-5">SUPPORT VECTOR MACHINE</div>
                            <div class="label">Predicted Sentiment: </div>
                            <div class="result">
                                <div id="csg_svc" class='is-size-4 has-text-weight-bold'></div>
                            </div>
                        </div>
                        <div class="cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                            <div class="label is-size-5">GRADIENT BOOSTING</div>
                            <div class="label">Predicted Sentiment: </div>
                            <div class="result">
                                <div id="csg_xgb" class='is-size-4 has-text-weight-bold'></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="tabs-4">
                    <div class="columns">
                        <div class="column is-3">
                            <div class="box m-1">
                                <div class="field">
                                    <p class="title is-6">Model Select<span class="required">*</span></p>
                                    <div class="select">
                                        <select id="model-lists" required name="model-lists">
                                        </select>
                                    </div>
                                </div>

                                <div class="field">
                                    <p class="control">
                                        <button id="mv_predict" class="button is-primary is-fullwidth" onclick="self_predict()">
                                            Get Prediction
                                        </button>
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="column">
                            <div class="box ">
                                <div class="grid">
                                    <div id="st-results" class="is-hidden cell has-background-light has-text-primary-invert has-radius-normal p-3 mt-2 has-text-centered">
                                        <div id="model-used" class="label is-size-5"></div>
                                        <div class="label">Predicted Sentiment: </div>
                                        <div class="result">
                                            <div id="model-result" class='is-size-4 has-text-weight-bold'></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        const predict = function(url, data, fn) {
            fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "evaluatee": data.evaluatee,
                        "position": data.position,
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
                .then(fn);
        }

        // Get the list of models created in models/retrain folder
        fetch("http://localhost:8000/get_models")
            .then(response => response.json())
            .then(data => {
                let model_list = ""
                model_list += `<option value=''>---Select Model---</option>`
                data.forEach(function(d, i) {
                    model_list += `<option value='${d}'>${d}</option>`
                });

                document.getElementById('model-lists').innerHTML = model_list;
            });


        let request_params = JSON.parse(JSON.stringify(<?php echo json_encode($_POST); ?>))

        predict('http://localhost:8000/predict', request_params, data => {
            let knn_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
            let svc_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
            let xgb_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
            let rfc_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
            let lr_pred = '<span style="font-size: 4em;">😊</span><br>Positive';

            let csg_knn_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
            let csg_svc_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
            let csg_xgb_pred = '<span style="font-size: 4em;">😊</span><br>Positive';

            let knn_class = "has-text-success";
            let svc_class = "has-text-success";
            let xgb_class = "has-text-success";
            let rfc_class = "has-text-success";
            let lr_class = "has-text-success";

            let csg_knn_class = "has-text-success";
            let csg_svc_class = "has-text-success";
            let csg_xgb_class = "has-text-success";

            let actual_sent = "has-text-success"

            if (data.knn_prediction == 0) {
                knn_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                knn_class = 'has-text-link-light'
            } else if (data.knn_prediction > 1) {
                knn_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                knn_class = 'has-text-danger'
            }

            if (data.svc_prediction == 0) {
                svc_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                svc_class = 'has-text-link-light'
            } else if (data.svc_prediction > 1) {
                svc_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                svc_class = 'has-text-danger'
            }

            if (data.xgb_prediction == 0) {
                xgb_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                xgb_class = 'has-text-link-light'
            } else if (data.xgb_prediction > 1) {
                xgb_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                xgb_class = 'has-text-danger'
            }

            if (data.rfc_prediction == 0) {
                rfc_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                rfc_class = 'has-text-link-light'
            } else if (data.rfc_prediction > 1) {
                rfc_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                rfc_class = 'has-text-danger'
            }

            if (data.lr_prediction == 0) {
                lr_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                lr_class = 'has-text-link-light'
            } else if (data.lr_prediction > 1) {
                lr_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                lr_class = 'has-text-danger'
            }

            // =========

            if (data.csg_knn_prediction == 0) {
                csg_knn_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                csg_knn_class = 'has-text-link-light'
            } else if (data.csg_knn_prediction > 1) {
                csg_knn_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                csg_knn_class = 'has-text-danger'
            }

            if (data.csg_svc_prediction == 0) {
                csg_svc_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                csg_svc_class = 'has-text-link-light'
            } else if (data.csg_svc_prediction > 1) {
                csg_svc_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                csg_svc_class = 'has-text-danger'
            }

            if (data.csg_xgb_prediction == 0) {
                csg_xgb_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                csg_xgb_class = 'has-text-link-light'
            } else if (data.csg_xgb_prediction > 1) {
                csg_xgb_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                csg_xgb_class = 'has-text-danger'
            }


            if (data.sentiment_class == "NEUTRAL") {
                actual_sent = 'has-text-link-light'
            } else if (data.sentiment_class == "NEGATIVE") {
                actual_sent = 'has-text-danger'
            }

            document.getElementById('knn').innerHTML = knn_pred;
            document.getElementById('knn').classList.add(knn_class);

            document.getElementById('svc').innerHTML = svc_pred;
            document.getElementById('svc').classList.add(svc_class);

            document.getElementById('xgb').innerHTML = xgb_pred;
            document.getElementById('xgb').classList.add(xgb_class);

            document.getElementById('rfc').innerHTML = rfc_pred;
            document.getElementById('rfc').classList.add(rfc_class);

            document.getElementById('lr').innerHTML = lr_pred;
            document.getElementById('lr').classList.add(lr_class);


            document.getElementById('csg_knn').innerHTML = csg_knn_pred;
            document.getElementById('csg_knn').classList.add(csg_knn_class);

            document.getElementById('csg_svc').innerHTML = csg_svc_pred;
            document.getElementById('csg_svc').classList.add(csg_svc_class);

            document.getElementById('csg_xgb').innerHTML = csg_xgb_pred;
            document.getElementById('csg_xgb').classList.add(csg_xgb_class);

            document.getElementById('actual_pred').textContent = data.sentiment_class
            document.getElementById('actual_pred').classList.add(actual_sent);
        });

        const self_predict = function() {
            let selected_model = document.getElementById('model-lists').value
            if (selected_model == "") {
                alert("No model selected.")
            } else {
                document.getElementById('st-results').classList.add('is-hidden')
                predict(`http://localhost:8000/predict?model=${selected_model}`, request_params, data => {
                    let st_pred = '<span style="font-size: 4em;">😊</span><br>Positive';
                    let st_class = "has-text-success";

                    if (data.self_train_prediction == 0) {
                        st_pred = '<span style="font-size: 4em;">😐</span><br>Neutral'
                        st_class = 'has-text-link-light'
                    } else if (data.self_train_prediction > 1) {
                        st_pred = '<span style="font-size: 4em;">😡</span><br>Negative'
                        st_class = 'has-text-danger'
                    }

                    document.getElementById('model-used').textContent = selected_model;
                    document.getElementById('model-result').innerHTML = st_pred;
                    document.getElementById('model-result').classList.add(st_class);
                    document.getElementById('st-results').classList.remove('is-hidden')
                })
            }
        }
    </script>

    <script src="result.js"></script>
</body>

</html>