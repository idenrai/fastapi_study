<script>
  import { link } from 'svelte-spa-router'
  import { page, keyword, access_token, username, is_login } from '../lib/store'
</script>

<!--
   네비게이션바
   https://getbootstrap.com/docs/5.2/components/navbar/
 -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom">
  <div class="container-fluid">
    <a
      use:link
      class="navbar-brand"
      href="/"
      on:click={() => {
        $page = 0
        $keyword = ''
      }}>FastAPI Study</a
    >
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon" />
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        \ {#if $is_login}
          <li class="nav-item">
            <a
              use:link
              class="nav-link"
              href="/user-login"
              on:click={() => {
                $access_token = ''
                $username = ''
                $is_login = false
              }}>로그아웃</a
            >
          </li>
        {:else}
          <li class="nav-item">
            <a use:link class="nav-link" href="/user-create">회원가입</a>
          </li>
          <li class="nav-item">
            <a use:link class="nav-link" href="/user-login">로그인</a>
          </li>
        {/if}
      </ul>
    </div>
  </div>
</nav>
