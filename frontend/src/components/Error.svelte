<!-- 
    error를 전달받아 오류를 표시
 -->
<script>
  // 전달받은 에러의 속성 지정
  export let error
</script>

{#if typeof error.detail === 'string'}
  <div class="alert alert-danger" role="alert">
    <div>
      {error.detail}
    </div>
  </div>
{:else if typeof error.detail === 'object' && error.detail.length > 0}
  <div class="alert alert-danger" role="alert">
    {#each error.detail as err, i}
      <div>
        <strong>{err.loc[1]}</strong> : {err.msg}
      </div>
    {/each}
  </div>
{/if}
