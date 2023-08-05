<script>
  import { link, push } from 'svelte-spa-router'

  import fastapi from '../lib/api'
  import Error from '../components/Error.svelte'
  import moment from 'moment/min/moment-with-locales'

  moment.locale('ko')

  export let params = {}
  let question_id = params.question_id

  // question은 질문 한 건에 대한 상세 정보이므로, {} 로 초기화 필요
  let question = { answers: [] }
  let content = ''
  let error = { detail: [] }

  function get_question() {
    const url = '/api/question/detail/' + question_id
    fastapi('get', url, {}, (json) => {
      question = json
    })
  }

  get_question()

  function post_answer(event) {
    event.preventDefault()
    const url = '/api/answer/create/' + question_id
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

<div class="container my-3">
  <!-- 질문 -->
  <h2 class="border-bottom py-2">{question.subject}</h2>
  <div class="card my-3">
    <div class="card-body">
      <div class="card-text" style="white-space: pre-line;">{question.content}</div>
      <div class="d-flex justify-content-end">
        <div class="badge bg-light text-dark p-2">
          {moment(question.create_date).format('YYYY년 MM월 DD일 HH:mm')}
        </div>
      </div>
    </div>
  </div>

  <!-- 에러 -->
  <Error {error} />

  <button
    class="btn btn-secondary"
    on:click={() => {
      push('/')
    }}>목록으로</button
  >

  <!-- 답변 입력 -->
  <form metohd="post" class="my-3">
    <div class="mb-3">
      <textarea class="form-control" rows="5" bind:value={content} />
    </div>
    <input type="submit" value="답변 등록" class="btn btn-primary" on:click={post_answer} />
  </form>

  <!-- 답변수 -->
  <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>

  <!-- 답변 목록 -->
  {#each question.answers as answer}
    <div class="card my-3">
      <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
        <div class="d-flex justify-content-end">
          <div class="badge bg-light text-dark p-1">
            {moment(answer.create_date).format('YYYY년 MM월 DD일 HH:mm')}
          </div>
        </div>
      </div>
    </div>
  {/each}
</div>
