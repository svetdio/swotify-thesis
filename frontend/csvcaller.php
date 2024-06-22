<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Collect form data
    $evaluatee = $_POST['evaluatee']
    $position = $_POST['position']
    $responsibility_rating = $_POST['responsibility_rating']
    $team_communication_rating = $_POST['team_communication_rating']
    $task_delegation_rating = $_POST['task_delegation_rating']
    $calmness_rating = $_POST['calmness_rating']
    $adaptability_rating = $_POST['adaptability_rating']
    $attitude_rating = $_POST['attitude_rating']
    $comm_collab_rating = $_POST['comm_collab_rating']
    $external_resp_rating = $_POST['external_resp_rating']
    $time_management_rating = $_POST['time_management_rating']
    $collab_rating = $_POST['collab_rating']
    $flexible_rating = $_POST['flexible_rating']
    $accountability_rating = $_POST['accountability_rating']
    $event_contribution = $_POST['event_contribution']
    $comment_feedback = $_POST['comment_feedback'] 
    
    // URL of the CSV file
    $url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR-R5kcjJsU1VcaWMuZG4naPz52sppvlvVPLGbqNqww-QqvDt7xTMHumiFkHFQu0WxeBZ6z3ziqjIZJ/pub?output=csv';
    
    // Local file path to save the downloaded CSV
    $localFile = 'data.csv';
    
    // Download the CSV file
    file_put_contents($localFile, file_get_contents($url));
    
    // Open the file for appending
    $handle = fopen($localFile, 'a');
    
    // Append the new data
    fputcsv($handle, [$responsibility_rating, $team_communication_rating, $task_delegation_rating, $calmness_rating, $adaptability_rating, $attitude_rating, $comm_collab_rating, $external_resp_rating, $time_management_rating, $collab_rating,  $flexible_rating, $accountability_rating, $event_contribution, $comment_feedback]);
    
    // Close the file
    fclose($handle);
    
    // Optional: Upload the updated CSV file back to the web (requires additional steps)
    
    echo "Data successfully saved!";
}
?>
