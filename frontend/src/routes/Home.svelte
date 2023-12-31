<script>
  import { link } from 'svelte-spa-router'
  import moment from 'moment/min/moment-with-locales'

  import fastapi from '../lib/api'
  import { page, is_login, keyword } from '../lib/store'

  moment.locale('ko')

  let question_list = []
  let size = 10
  let total = 0
  let kw = ''
  let first_loc_page = 0
  let last_loc_page = 9

  // svelte에서 변수 앞에 $: 가 붙으면 반응형 변수
  // https://svelte.dev/tutorial/reactive-statements
  $: total_page = Math.ceil(total / size)

  function get_question_list() {
    const url = '/questions'

    let params = {
      page: $page,
      size: size,
      keyword: $keyword,
    }
    fastapi('get', url, params, (json) => {
      question_list = json.question_list
      total = json.total
      kw = $keyword
    })
  }

  // page, keyword값이 변경될 경우, get_question_list 함수도 다시 호출
  $: $page, $keyword, get_question_list()
</script>

<div class="container my-3">
  <div class="row my-3">
    <div class="col-6">
      <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
    </div>
    <div class="col-6">
      <div class="input-group">
        <input type="text" class="form-control" bind:value={kw} />
        <button
          class="btn btn-outline-secondary"
          on:click={() => {
            $keyword = kw
            $page = 0
          }}>찾기</button
        >
      </div>
    </div>
  </div>

  <table class="text-center table">
    <thead>
      <tr>
        <th>번호</th>
        <th class="text-start" style="width:50%">제목</th>
        <th>글쓴이</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
        <tr class="text-center">
          <td>{total - $page * size - i}</td>
          <td class="text-start">
            <!--
                해시 기반 라우팅
                a 태그에 use:link 를 사용, 항상 /# 이 선행되도록 경로를 만들 것
                브라우저가 /# 으로 시작하는 URL을 동일 페이지로 인식하게 되므로, 리플레쉬시 서버로 페이지 요청을 안보냄
                => Frontend에서만 사용하는 경로를 API에 요청하는 일이 없어짐
            -->
            <a use:link href="/detail/{question.id}">
              {question.subject}
            </a>
            {#if question.answers.length > 0}
              <span class="text-danger small mx-2">{question.answers.length}</span>
            {/if}
          </td>
          <td>
            {question.user ? question.user.username : ''}
          </td>
          <td>{moment(question.create_date).format('YYYY년 MM월 DD일 HH:mm')}</td>
        </tr>
      {/each}
    </tbody>
  </table>
  <!-- 페이징처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 첫페이지 -->
    <li class="page-item {$page == 0 && 'disabled'}">
      <button class="page-link" on:click={() => ($page = 0)}>&langle;&langle;</button>
    </li>
    <!-- 이전페이지 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      <button class="page-link" on:click={() => $page--}>&langle;</button>
    </li>
    <!-- 페이지번호 -->
    {#each Array(total_page) as _, loop_page}
      {#if loop_page >= first_loc_page && loop_page <= last_loc_page}
        <li class="page-item {loop_page === $page && 'active'}">
          <button on:click={() => ($page = loop_page)} class="page-link">{loop_page + 1}</button>
        </li>
      {/if}
    {/each}
    <!-- 다음페이지 -->
    <li class="page-item {$page >= total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => $page++}>&rangle;</button>
    </li>
    <!-- 마지막 페이지 -->
    <li class="page-item {$page == total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => ($page = total_page - 1)}>&rangle;&rangle;</button>
    </li>
  </ul>
  <!-- 페이징처리 끝 -->
</div>
