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

export function finishActivity(expense) {
  return fetch(`/api/expense/update/${expense.id}`, {
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

export function getTodaysActivityGroups(date) {
  let queryDate = date;
  if(!queryDate) {
    queryDate = new Date().toISOString().substr(0,10)
  }
  return fetch(`/api/expense/groups/${queryDate}`, {
    method: 'GET',
  })
  .then(res => res.json())
  .then(response => response)
  .catch(error => console.error('Error:', error))
}
