const home = new Vue({
  el: '#home',
  data: {
    selectedSkill: '',
    selectedAmountOfTime: 15,
    isActivityStarted: false,
    timeProgressBarText: "",
    timerProgress: 0,
    activityTimer: null,
  },
  methods: {
    onActivityStart,
    onActivityStop,
  }
})

function clearProgress() {
  const timeProgressBar = document.querySelector("#time-progressbar");
  timeProgressBar.setAttribute("aria-valuenow", '0');
  timeProgressBar.style.width = '0';

  this.isActivityStarted = false;
  this.timerProgress = 0;
  this.timeProgressBarText = ''
  clearInterval(this.activityTimer);
}

function onActivityStart() {
  this.isActivityStarted = true;
  const timeProgressBar = document.querySelector("#time-progressbar");
  const amountOfTime = this.selectedAmountOfTime * 60;
  // const timeProgressBarText = document.querySelector("#time-progressbar-text");
  const percentsOfTimePerSecond = 100/(+amountOfTime);
  // TODO move timeprogressBar to component
  this.timeProgressBarText = `${this.timerProgress}/${amountOfTime} seconds`
  // timeProgressBarText.innerHTML = `${timerProgress}/${amountOfTime} seconds`;

  this.activityTimer = setInterval(() => {
    this.timerProgress++;
    if(this.timerProgress >= amountOfTime) {
      clearProgress.apply(this);
    }
    let timerProgressInPercents = this.timerProgress*percentsOfTimePerSecond;
    timeProgressBar.setAttribute("aria-valuenow", timerProgressInPercents);
    timeProgressBar.style.width = `${timerProgressInPercents}%`;
    this.timeProgressBarText = `${this.timerProgress}/${amountOfTime} seconds`;
  }, 1000)
}

function onActivityStop() {
  if(window.confirm("If you stop activity progress will be lost. (Sorry, there isn't pause - you can't pause the time.)")) {
    clearProgress.apply(this);
  }
}

(function() {
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
})()
