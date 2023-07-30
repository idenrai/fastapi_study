<script>
  import { link } from 'svelte-spa-router'

  import fastapi from '../lib/api'
  import Error from '../components/Error.svelte'

  export let params = {}
  let question_id = params.question_id

  // question은 질문 한 건에 대한 상세 정보이므로, {} 로 초기화 필요
  let question = { answers: [] }
  let content = ''
  let error = { detail: [] }

  function get_question() {
    let url = '/api/question/detail/' + question_id
    fastapi('get', url, {}, (json) => {
      question = json
    })
  }

  get_question()

  function post_answer(event) {
    event.preventDefault()
    let url = '/api/answer/create/' + question_id
    let params = {
      content: content,
    }
    fastapi(
      'post',
      url,
      params,
      (json) => {
        content = ''
        error = { detail: [] }
        get_question()
      },
      (err_json) => {
        error = err_json
      }
    )
  }
</script>

<h1>{question.subject}</h1>
<div>{question.content}</div>
<ul>
  {#each question.answers as answer}
    <li>{answer.content}</li>
  {/each}
</ul>
<br />
<Error {error} />
<br />
<form metohd="post">
  <textarea rows="15" bind:value={content} />
  <input type="submit" value="답변 등록" on:click={post_answer} />
</form>
<br />
<a use:link href="/"> 돌아가기 </a>
