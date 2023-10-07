<script>
  import fastapi from '../lib/api'
  import { push } from 'svelte-spa-router'
  import Error from '../components/Error.svelte'

  export let params = {}
  const answer_id = params.answer_id

  let error = { detail: [] }
  let question_id = 0
  let content = ''

  fastapi('get', '/answers/detail/' + answer_id, {}, (json) => {
    question_id = json.question_id
    content = json.content
  })

  function update_answer(event) {
    event.preventDefault()
    const url = '/answers'
    let params = {
      answer_id: answer_id,
      content: content,
    }
    fastapi(
      'put',
      url,
      params,
      (json) => {
        push('/detail/' + question_id)
      },
      (err_json) => {
        error = err_json
      }
    )
  }
</script>

<div class="container">
  <h5 class="my-3 border-bottom pb-2">답변 수정</h5>
  <Error {error} />
  <form method="post" class="my-3">
    <div class="mb-3">
      <label for="content">내용</label>
      <textarea class="form-control" rows="10" bind:value={content} />
    </div>
    <button class="btn btn-primary" on:click={update_answer}>수정하기</button>
  </form>
</div>
