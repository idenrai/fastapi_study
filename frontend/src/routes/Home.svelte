<script>
  import fastapi from '../lib/api'
  import { link } from 'svelte-spa-router'

  let question_list = []

  function get_question_list() {
    fastapi('get', '/api/question/list', {}, (json) => {
      question_list = json
    })
  }

  get_question_list()
</script>

<div class="container my-3">
  <table class="table">
    <thead>
      <tr>
        <td>번호</td>
        <td>제목</td>
        <td>작성일시</td>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
        <tr>
          <td>{i + 1}</td>
          <td>
            <!--
                해시 기반 라우팅
                a 태그에 use:link 를 사용, 항상 /# 이 선행되도록 경로를 만들 것
                브라우저가 /# 으로 시작하는 URL을 동일 페이지로 인식하게 되므로, 리플레쉬시 서버로 페이지 요청을 안보냄
                => Frontend에서만 사용하는 경로를 API에 요청하는 일이 없어짐
            -->
            <a use:link href="/detail/{question.id}">
              {question.subject}
            </a>
          </td>
          <td>{question.create_date}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
