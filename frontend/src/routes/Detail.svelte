<script>
  import fastapi from '../lib/api'
  import { link } from 'svelte-spa-router'

  export let params = {}
  let question_id = params.question_id

  // question은 질문 한 건에 대한 상세 정보이므로, {} 로 초기화 필요
  let question = {}

  function get_question() {
    fastapi('get', '/api/question/detail/' + question_id, {}, json => {
      question = json
    })
  }

  get_question()
</script>

<h1>{question.subject}</h1>
<div>{question.content}</div>
<br />
<a use:link href="/"> 돌아가기 </a>
