<!DOCTYPE html>

<head>
    <title>SWOTIFY SA Form</title>
    <!-- <script src="script.js"></script> -->
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="icon" href="assets/sentiment-analysis.png">
</head>

<body>
    <form id="sentimentForm" method="POST" action="result.php">
        <div class="form">
            <div class="title-div">
                <h1>MODEL VALIDATION</h1>
            </div>

            <!-- <div class="rate">
                <b>Legend:</b><br>
                <br>5- Strongly Agree
                <br>4- Agree
                <br>3- Neutral
                <br>2- Disagree
                <br>1- Strongly Disagree

                <br><br><span class="required"> Required *</span>
            </div> -->

            <div class="rate">
                He/She was well-prepared for his/her responsibilities during the Local CAF 2024?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="responsibility_rating_rating5" name="responsibility_rating" value="5" required>
                <label for="responsibility_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="responsibility_rating_rating4" name="responsibility_rating" value="4" required>
                <label for="responsibility_rating_rating4">Agree</label><br>
                <input type="radio" id="responsibility_rating_rating3" name="responsibility_rating" value="3" required>
                <label for="responsibility_rating_rating3">Neutral</label><br>
                <input type="radio" id="responsibility_rating_rating2" name="responsibility_rating" value="2" required>
                <label for="responsibility_rating_rating2">Disagree</label><br>
                <input type="radio" id="responsibility_rating_rating1" name="responsibility_rating" value="1" required>
                <label for="responsibility_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification"></div>
            </div>

            <div class="rate">
                He/She effectively communicated with his/her team members before and during the Local CAF 2024?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="team_communication_rating_rating5" name="team_communication_rating" value="5" required>
                <label for="team_communication_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="team_communication_rating_rating4" name="team_communication_rating" value="4" required>
                <label for="team_communication_rating_rating4">Agree</label><br>
                <input type="radio" id="team_communication_rating_rating3" name="team_communication_rating" value="3" required>
                <label for="team_communication_rating_rating3">Neutral</label><br>
                <input type="radio" id="team_communication_rating_rating2" name="team_communication_rating" value="2" required>
                <label for="team_communication_rating_rating2">Disagree</label><br>
                <input type="radio" id="team_communication_rating_rating1" name="team_communication_rating" value="1" required>
                <label for="team_communication_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification1"></div>
            </div>

            <div class="rate">
                He/She was able to delegate tasks effectively and ensure he/she were completed on time?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="task_delegation_rating_rating5" name="task_delegation_rating" value="5" required>
                <label for="task_delegation_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="task_delegation_rating_rating4" name="task_delegation_rating" value="4" required>
                <label for="task_delegation_rating_rating4">Agree</label><br>
                <input type="radio" id="task_delegation_rating_rating3" name="task_delegation_rating" value="3" required>
                <label for="task_delegation_rating_rating3">Neutral</label><br>
                <input type="radio" id="task_delegation_rating_rating2" name="task_delegation_rating" value="2" required>
                <label for="task_delegation_rating_rating2">Disagree</label><br>
                <input type="radio" id="task_delegation_rating_rating1" name="task_delegation_rating" value="1" required>
                <label for="task_delegation_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification2"></div>
            </div>

            <div class="rate">
                He/She remained calm and collected under pressure during the event?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="calmness_rating_rating5" name="calmness_rating" value="5" required>
                <label for="calmness_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="calmness_rating_rating4" name="calmness_rating" value="4" required>
                <label for="calmness_rating_rating4">Agree</label><br>
                <input type="radio" id="calmness_rating_rating3" name="calmness_rating" value="3" required>
                <label for="calmness_rating_rating3">Neutral</label><br>
                <input type="radio" id="calmness_rating_rating2" name="calmness_rating" value="2" required>
                <label for="calmness_rating_rating2">Disagree</label><br>
                <input type="radio" id="calmness_rating_rating1" name="calmness_rating" value="1" required>
                <label for="calmness_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification3"></div>
            </div>

            <div class="rate">
                He/She was able to adapt to unexpected challenges and changes before or during the Local CAF 2024?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="adaptability_rating_rating5" name="adaptability_rating" value="5" required>
                <label for="adaptability_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="adaptability_rating_rating4" name="adaptability_rating" value="4" required>
                <label for="adaptability_rating_rating4">Agree</label><br>
                <input type="radio" id="adaptability_rating_rating3" name="adaptability_rating" value="3" required>
                <label for="adaptability_rating_rating3">Neutral</label><br>
                <input type="radio" id="adaptability_rating_rating2" name="adaptability_rating" value="2" required>
                <label for="adaptability_rating_rating2">Disagree</label><br>
                <input type="radio" id="adaptability_rating_rating1" name="adaptability_rating" value="1" required>
                <label for="adaptability_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification4"></div>
            </div>

            <div class="rate">
                He/She consistently displayed a positive and enthusiastic attitude throughout the Local CAF 2024?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="attitude_rating_rating5" name="attitude_rating" value="5" required>
                <label for="attitude_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="attitude_rating_rating4" name="attitude_rating" value="4" required>
                <label for="attitude_rating_rating4">Agree</label><br>
                <input type="radio" id="attitude_rating_rating3" name="attitude_rating" value="3" required>
                <label for="attitude_rating_rating3">Neutral</label><br>
                <input type="radio" id="attitude_rating_rating2" name="attitude_rating" value="2" required>
                <label for="attitude_rating_rating2">Disagree</label><br>
                <input type="radio" id="attitude_rating_rating1" name="attitude_rating" value="1" required>
                <label for="attitude_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification5"></div>
            </div>

            <div class="rate">
                Do you think he/she face any difficulties with communication or collaboration during the event?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="comm_collab_rating_rating5" name="comm_collab_rating" value="1" required>
                <label for="comm_collab_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="comm_collab_rating_rating4" name="comm_collab_rating" value="2" required>
                <label for="comm_collab_rating_rating4">Agree</label><br>
                <input type="radio" id="comm_collab_rating_rating3" name="comm_collab_rating" value="3" required>
                <label for="comm_collab_rating_rating3">Neutral</label><br>
                <input type="radio" id="comm_collab_rating_rating2" name="comm_collab_rating" value="4" required>
                <label for="comm_collab_rating_rating2">Disagree</label><br>
                <input type="radio" id="comm_collab_rating_rating1" name="comm_collab_rating" value="5" required>
                <label for="comm_collab_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification6"></div>
            </div>

            <div class="rate">
                In any external factors that threatened the success of the event, did he/she respond relatively?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="external_resp_rating_rating5" name="external_resp_rating" value="5" required>
                <label for="external_resp_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="external_resp_rating_rating4" name="external_resp_rating" value="4" required>
                <label for="external_resp_rating_rating4">Agree</label><br>
                <input type="radio" id="external_resp_rating_rating3" name="external_resp_rating" value="3" required>
                <label for="external_resp_rating_rating3">Neutral</label><br>
                <input type="radio" id="external_resp_rating_rating2" name="external_resp_rating" value="2" required>
                <label for="external_resp_rating_rating2">Disagree</label><br>
                <input type="radio" id="external_resp_rating_rating1" name="external_resp_rating" value="1" required>
                <label for="external_resp_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification7"></div>
            </div>

            <div class="rate">
                He/She did not effectively manage his/her time during the event?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="time_management_rating_rating5" name="time_management_rating" value="1" required>
                <label for="time_management_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="time_management_rating_rating4" name="time_management_rating" value="2" required>
                <label for="time_management_rating_rating4">Agree</label><br>
                <input type="radio" id="time_management_rating_rating3" name="time_management_rating" value="3" required>
                <label for="time_management_rating_rating3">Neutral</label><br>
                <input type="radio" id="time_management_rating_rating2" name="time_management_rating" value="4" required>
                <label for="time_management_rating_rating2">Disagree</label><br>
                <input type="radio" id="time_management_rating_rating1" name="time_management_rating" value="5" required>
                <label for="time_management_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification8"></div>
            </div>

            <div class="rate">
                He/She did not collaborate effectively with other CSG officers or committees?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="collab_rating_rating5" name="collab_rating" value="1" required>
                <label for="collab_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="collab_rating_rating4" name="collab_rating" value="2" required>
                <label for="collab_rating_rating4">Agree</label><br>
                <input type="radio" id="collab_rating_rating3" name="collab_rating" value="3" required>
                <label for="collab_rating_rating3">Neutral</label><br>
                <input type="radio" id="collab_rating_rating2" name="collab_rating" value="4" required>
                <label for="collab_rating_rating2">Disagree</label><br>
                <input type="radio" id="collab_rating_rating1" name="collab_rating" value="5" required>
                <label for="collab_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification9"></div>
            </div>

            <div class="rate">
                He/She was not flexible in his/her approach to problem-solving during the Local CAF 2024?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="flexible_rating_rating5" name="flexible_rating" value="1" required>
                <label for="flexible_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="flexible_rating_rating4" name="flexible_rating" value="2" required>
                <label for="flexible_rating_rating4">Agree</label><br>
                <input type="radio" id="flexible_rating_rating3" name="flexible_rating" value="3" required>
                <label for="flexible_rating_rating3">Neutral</label><br>
                <input type="radio" id="flexible_rating_rating2" name="flexible_rating" value="4" required>
                <label for="flexible_rating_rating2">Disagree</label><br>
                <input type="radio" id="flexible_rating_rating1" name="flexible_rating" value="5" required>
                <label for="flexible_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification10"></div>
            </div>

            <div class="rate">
                He/She did not take responsibility for his/her mistakes or the mistakes of his/her team?
                <span class="required">*</span>
                <br><br>
                <input type="radio" id="accountability_rating_rating5" name="accountability_rating" value="1" required>
                <label for="accountability_rating_rating5">Strongly Agree</label><br>
                <input type="radio" id="accountability_rating_rating4" name="accountability_rating" value="2" required>
                <label for="accountability_rating_rating4">Agree</label><br>
                <input type="radio" id="accountability_rating_rating3" name="accountability_rating" value="3" required>
                <label for="accountability_rating_rating3">Neutral</label><br>
                <input type="radio" id="accountability_rating_rating2" name="accountability_rating" value="4" required>
                <label for="accountability_rating_rating2">Disagree</label><br>
                <input type="radio" id="accountability_rating_rating1" name="accountability_rating" value="5" required>
                <label for="accountability_rating_rating1">Strongly Disagree</label>
                <div class="notification" id="notification11"></div>
            </div>

            <div class="sentiment1">
                <div class="name">
                    What do you think is his/her greatest contribution and what opportunity did he/she unlock during Local CAF 2024 event?
                    <span class="required">*</span>
                </div>
                <div class="input-div">
                    <textarea name="event_contribution" placeholder="Your answer" required></textarea>
                    <div class="notification" id="notification"></div>
                </div>
            </div>

            <div class="sentiment2">
                <div class="name">
                    Do you have any comment, suggestion/s, and recommendation/s?
                    <span class="required">*</span>
                </div>
                <div class="input-div">
                    <textarea name="comment_feedback" placeholder="Your answer" required></textarea>
                    <div class="notification" id="notification"></div>
                </div>
            </div>

            <div>
                <input class="button" type="submit" name="Submit" value="SUBMIT" style="font-weight: bold;">
            </div>
    </form>
</body>