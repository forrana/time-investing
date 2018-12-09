export function startActivity(expense) {
  return fetch("/api/expense/create", {
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
  .then(response => response.expense._id.$oid)
  .catch(error => console.error('Error:', error))
}

export function finishActivity(expenseId) {
  return fetch(`/api/expense/update/${expenseId}`, {
    method: 'POST',
    body: JSON.stringify( {
      finished_at: new Date().toISOString().substr(0,19)
    } ), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  })
  .then(res => res.json())
  .then(response => response.expense)
  .catch(error => console.error('Error:', error))
}

export function getTodaysActivityGroups() {
  // today
  let startDate = new Date().toISOString().substr(0,10);
  // tomorrow
  let endDate = new Date(new Date().setDate((new Date().getDate() + 1))).toISOString().substring(0,10);

  return fetch(`/api/expense/groups/${startDate}/${endDate}`, {
    method: 'GET',
  })
  .then(res => res.json())
  .then(response => response)
  .catch(error => console.error('Error:', error))
}

export function getThisWeekActivityGroups() {
  let currentDate = new Date(); // get current date
  let first = currentDate.getDate() - currentDate.getDay(); // First day is the day of the month - the day of the week
  let last = first + 6; // last day is the first day + 6
  //first day of the week
  let startDate = new Date(currentDate.setDate(first)).toISOString().substring(0,10);
  //last day of the week
  let endDate = new Date(currentDate.setDate(last)).toISOString().substring(0,10);

  return fetch(`/api/expense/groups/${startDate}/${endDate}`, {
    method: 'GET',
  })
  .then(res => res.json())
  .then(response => response)
  .catch(error => console.error('Error:', error))
}
