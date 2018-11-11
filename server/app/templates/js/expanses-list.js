const timeLeftElement = document.querySelector("#expenses-list-time-left")
const currentUnixTime = new Date().getTime() / 1000;
const endOfTheCurrentDay = (new Date()).setHours(23,59,59,999)
const endOfTheCurrentDayUnixTime = endOfTheCurrentDay / 1000

let minutesLeftInTheCurrentDay = (endOfTheCurrentDayUnixTime - currentUnixTime) / 60
minutesLeftInTheCurrentDay =  Math.round(minutesLeftInTheCurrentDay)
timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
setInterval(() => {
  if(minutesLeftInTheCurrentDay > 0)
    minutesLeftInTheCurrentDay--
  else location.reload();
  timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
}, 1000*60);


const onActivityStart = () => {
  let timerProgress = 0;
  const timeProgressBar = document.querySelector("#time-progressbar");
  const amountOfTime = document.querySelector("#amount-of-time").value * 60;
  const timeProgressBarText = document.querySelector("#time-progressbar-text");
  const percentsOfTimePerSecond = 100/(+amountOfTime);

  timeProgressBarText.innerHTML = `${timerProgress}/${amountOfTime} seconds`;

  const timeProgresseInterval = setInterval(() => {
    timerProgress++;
    if(timerProgress >= amountOfTime) {
      clearInterval(timeProgresseInterval)
    }
    timeProgressBar.setAttribute("aria-valuenow", timerProgress*percentsOfTimePerSecond);
    timeProgressBar.style.width = `${timerProgress*percentsOfTimePerSecond}%`;
    timeProgressBarText.innerHTML = `${timerProgress}/${amountOfTime} seconds`;
  }, 1000)
}
