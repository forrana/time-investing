const timeLeftElement = document.querySelector("#expenses-list-time-left")
const currentUnixTime = new Date().getTime() / 1000;
const endOfTheCurrentDay = (new Date()).setHours(23,59,59,999)
const endOfTheCurrentDayUnixTime = endOfTheCurrentDay / 1000
let minutesLeftInTheCurrentDay = (endOfTheCurrentDayUnixTime - currentUnixTime) / 60
minutesLeftInTheCurrentDay =  Math.round(minutesLeftInTheCurrentDay)
timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
setInterval(() => {
  minutesLeftInTheCurrentDay--
  timeLeftElement.innerHTML = minutesLeftInTheCurrentDay
}, 1000*60);
