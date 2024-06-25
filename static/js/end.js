const usernames = JSON.parse(localStorage.getItem('usernames'))
const DScore = document.querySelector ('#DScore')
const AScore = document.querySelector ('#AScore')
const SScore = document.querySelector ('#SScore')
const user = document.querySelector('#user')
const DepScore = localStorage.getItem('depressionScore') || 0;
const anx = localStorage.getItem('AnxietyScore') || 0;
const stress = localStorage.getItem('StressScore') || 0;
const endtext = document.querySelector ('#end-text')


let depressionScore = DepScore*2;
let anxietyScore = anx*2;
let stressScore = stress*2;

if (depressionScore >= 0 && depressionScore <= 9) {
    affectdep="Normal";
      } else if(depressionScore >= 10 && depressionScore <= 13) {
        // Handle other cases as needed
        affectdep="Mild";
      }else if(depressionScore >= 14 && depressionScore <= 20){
        affectdep="Moderate";
      }else if(depressionScore >= 21 && depressionScore <= 27){
        affectdep="Severe";
      }else{
        affectdep="Extremely Severe";
      }

if (anxietyScore >= 0 && anxietyScore <= 7) {
        affectAn="Normal";
          } else if(anxietyScore >= 8 && anxietyScore <= 9) {
            // Handle other cases as needed
            affectAn="Mild";
          }else if(anxietyScore >= 10 && anxietyScore <= 14){
            affectAn="Moderate";
          }else if(anxietyScore >= 15 && anxietyScore <= 19){
            affectAn="Severe";
          }else{
            affectAn="Extremely Severe";
          }

if (stressScore >= 0 && stressScore <= 14) {
            affectSt="Normal";
            } else if(stressScore >= 15 && stressScore <= 18) {
              // Handle other cases as needed
              affectSt="Mild";
            }else if(stressScore >= 19 && stressScore <= 25){
              affectSt="Moderate";
            }else if(stressScore >= 26 && stressScore <= 33){
              affectSt="Severe";
            }else{
              affectSt="Extremely Severe";
            }

            DScore.innerText = `Depression Score: ${DepScore} (${affectdep})`;
            AScore.innerText = `Anxiety Score: ${anx} (${affectAn})`;
            SScore.innerText = `Stress Score: ${stress} (${affectSt})`;
            user.innerText = `User: ${usernames}`;

            document.addEventListener('DOMContentLoaded', () => {
              document.getElementById('saveScoreBtn').addEventListener('click', () => {
                  $("#saveScoreBtn").css("display", "none");
              });
          });