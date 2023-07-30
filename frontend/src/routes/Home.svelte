<script>
  import fastapi from '../lib/api'
  let question_list = []

  function get_question_list() {
    fastapi('get', '/api/question/list', {}, json => {
      question_list = json
    })
  }

  get_question_list()
</script>

<ul>
  {#each question_list as question}
    <li>
      <div>
        <p>제목 : {question.subject}</p>
        <p>내용 : {question.content}</p>
      </div>
    </li>
  {/each}
</ul>
