export function startActivity(expense) {
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
  .then(response => { expense.id = response.expense._id.$oid; return expense })
  .catch(error => console.error('Error:', error))
}

export function finishActivity(expense) {
  fetch(`/api/expense/update/${expense.id}`, {
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
