<script>
  import fastapi from '../lib/api'
  import { push } from 'svelte-spa-router'
  import Error from '../components/Error.svelte'
  import { page, is_login } from '../lib/store'

  let error = { detail: [] }
  let subject = ''
  let content = ''

  function post_question(event) {
    event.preventDefault()
    const url = '/api/question/create'
    let params = {
      subject: subject,
      content: content,
    }
    fastapi(
      'post',
      url,
      params,
      (json) => {
        push('/')
      },
      (err_json) => {
        error = err_json
      }
    )

    // 질문 등록시에도 페이지 초기화
    $page = 0
  }
</script>

<div class="container">
  <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
  <Error {error} />
  <form method="post" class="my-3">
    <div class="mb-3">
      <label for="subject">제목</label>
      <input type="text" class="form-control" bind:value={subject} />
    </div>
    <div class="mb-3">
      <label for="content">내용</label>
      <textarea class="form-control" rows="10" bind:value={content} />
    </div>
    <button class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click={post_question}>저장하기</button>
  </form>
</div>
