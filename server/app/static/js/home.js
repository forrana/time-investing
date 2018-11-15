const home = new Vue({
  el: '#home',
  data: {
    selectedAmountOfTime: 15,
    isActivityStarted: false,
    timerProgress: 0,
    timePassedSec: 0,
    activityTimer: null,
    expense: {
      skill: '',
      amount: 15
    }
  },
  methods: {
    onActivityStart,
    onActivityStop,
  },
  computed: {
    timeProgressBarText: function () {
      if(!this.isActivityStarted) return "";
      return `${this.timerProgress}/${this.expense.amount * 60} seconds`;
    },
    timerProgressInPercents: function () {
      if(!this.isActivityStarted) return 0;
      const percentsOfTimePerSecond = 100/(+this.expense.amount * 60);
      return this.timerProgress*percentsOfTimePerSecond;
    }
  }
})

function clearProgress() {
  this.isActivityStarted = false;
  this.timerProgress = 0;
  clearInterval(this.activityTimer);
}

function onActivityStart() {
  startActivity(this.expense);
  this.isActivityStarted = true;
  this.activityTimer = setInterval(() => {
    this.timerProgress++;
    if(this.timerProgress >= this.expense.amount * 60) {
      clearProgress.apply(this);
    }
  }, 1000)
}

function onActivityStop() {
  if(window.confirm("If you stop activity progress will be lost. (Sorry, there isn't pause - you can't pause the time.)")) {
    clearProgress.apply(this);
  }
}

function startActivity(expense) {
  fetch("/api/expense/create", {
    method: 'POST',
    body: JSON.stringify( {
      ...expense,
      started_at: new Date().toISOString().substr(0,19)
    } ), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  })
  .then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:', error))
}

// Day time countdown
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
