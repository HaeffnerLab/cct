  


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>HaeffnerLabLattice/lattice/cdllservers/APTMotor/APTMotorServer.py at master · micramm/HaeffnerLabLattice</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon-precomposed" sizes="57x57" href="apple-touch-icon-114.png" />
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="apple-touch-icon-114.png" />
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="apple-touch-icon-144.png" />
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="apple-touch-icon-144.png" />

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.png" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="A3PIYEZg/N9pV4CVvS/MnqUXhol6/xe5c/y0DNbL8YY=" name="csrf-token" />

    <link href="https://a248.e.akamai.net/assets.github.com/assets/github-796faf7daca344ef5dff71a6ed00c57b88a5f613.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="https://a248.e.akamai.net/assets.github.com/assets/github2-8fbba53285e1ba0adf5aaa39e8b0d8ab6c91d88b.css" media="screen" rel="stylesheet" type="text/css" />
    


    <script src="https://a248.e.akamai.net/assets.github.com/assets/frameworks-ac63e4a1fc7b5030f8c99d5200722f51ed8e7baa.js" type="text/javascript"></script>
    <script defer="defer" src="https://a248.e.akamai.net/assets.github.com/assets/github-b4c07f78e6c6bbda967b3071f067d7fe7587ab18.js" type="text/javascript"></script>
    

      <link rel='permalink' href='/micramm/HaeffnerLabLattice/blob/0549a77bdb10ed62f3f0be14f802e7f8f184930a/lattice/cdllservers/APTMotor/APTMotorServer.py'>
    <meta property="og:title" content="HaeffnerLabLattice"/>
    <meta property="og:type" content="githubog:gitrepository"/>
    <meta property="og:url" content="https://github.com/micramm/HaeffnerLabLattice"/>
    <meta property="og:image" content="https://a248.e.akamai.net/assets.github.com/images/gravatars/gravatar-user-420.png?1345673562"/>
    <meta property="og:site_name" content="GitHub"/>
    <meta property="og:description" content="Contribute to HaeffnerLabLattice development by creating an account on GitHub."/>

    <meta name="description" content="Contribute to HaeffnerLabLattice development by creating an account on GitHub." />
  <link href="https://github.com/micramm/HaeffnerLabLattice/commits/master.atom" rel="alternate" title="Recent Commits to HaeffnerLabLattice:master" type="application/atom+xml" />

  </head>


  <body class="logged_in page-blob linux vis-public env-production ">
    <div id="wrapper">

    
    

      <div id="header" class="true clearfix">
        <div class="container clearfix">
          <a class="site-logo " href="https://github.com/">
            <img alt="GitHub" class="github-logo-4x" height="30" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7@4x.png?1337118071" />
            <img alt="GitHub" class="github-logo-4x-hover" height="30" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7@4x-hover.png?1337118071" />
          </a>

            <a href="/notifications" class="notification-indicator tooltipped downwards" title="You have no unread notifications">
              <span class="mail-status all-read"></span>
            </a>

              
    <div class="topsearch command-bar-activated">
      <form accept-charset="UTF-8" action="/search" class="command_bar_form" id="top_search_form" method="get">
  <a href="/search" class="advanced-search tooltipped downwards command-bar-search" id="advanced_search" title="Advanced Search"><span class="mini-icon mini-icon-advanced-search "></span></a>
  <input type="text" name="q" id="command-bar" placeholder="Search or Type a Command" tabindex="1" />
  <span class="mini-icon help tooltipped downwards" title="Show Command Bar Help"></span>
  <input type="hidden" name="type" value="Everything" />
  <input type="hidden" name="repo" value="" />
  <input type="hidden" name="langOverride" value="" />
  <input type="hidden" name="start_value" value="1" />
</form>

      <ul class="top-nav">
          <li class="explore"><a href="https://github.com/explore">Explore</a></li>
          <li><a href="https://gist.github.com">Gist</a></li>
          <li><a href="/blog">Blog</a></li>
        <li><a href="http://help.github.com">Help</a></li>
      </ul>
    </div>


            


  
  <div id="userbox">
    <div id="user">
      <a href="https://github.com/soenkemoeller"><img height="20" src="https://secure.gravatar.com/avatar/181517bdbcffebd9ff964d9a23658e98?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="20" /></a>
      <a href="https://github.com/soenkemoeller" class="name">soenkemoeller</a>
    </div>
    <ul id="user-links">
      <li>
        <a href="/new" id="new_repo" class="tooltipped downwards" title="Create a New Repo"><span class="mini-icon mini-icon-create"></span></a>
      </li>
      <li>
        <a href="/settings/profile" id="account_settings"
          class="tooltipped downwards"
          title="Account Settings ">
          <span class="mini-icon mini-icon-account-settings"></span>
        </a>
      </li>
      <li>
          <a href="/logout" data-method="post" id="logout" class="tooltipped downwards" title="Sign Out">
            <span class="mini-icon mini-icon-logout"></span>
          </a>
      </li>
    </ul>
  </div>



          
        </div>
      </div>

      

      


            <div class="site hfeed" itemscope itemtype="http://schema.org/WebPage">
      <div class="container hentry">
        
        <div class="pagehead repohead instapaper_ignore readability-menu">
        <div class="title-actions-bar">
          


              <ul class="pagehead-actions">

          <li class="subscription">
              <form accept-charset="UTF-8" action="/notifications/subscribe" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="A3PIYEZg/N9pV4CVvS/MnqUXhol6/xe5c/y0DNbL8YY=" /></div>  <input id="repository_id" name="repository_id" type="hidden" value="2015629" />
  <div class="context-menu-container js-menu-container js-context-menu">
    <span class="minibutton switcher bigger js-menu-target">
      <span class="js-context-button">
          <span class="mini-icon mini-icon-watching"></span>Watch
      </span>
    </span>

    <div class="context-pane js-menu-content">
      <a href="javascript:;" class="close js-menu-close"><span class="mini-icon mini-icon-remove-close"></span></a>
      <div class="context-title">Notification status</div>

      <div class="context-body pane-selector">
        <ul class="js-navigation-container">
          <li class="selector-item js-navigation-item js-navigation-target selected">
            <span class="mini-icon mini-icon-confirm"></span>
            <label>
              <input checked="checked" id="do_included" name="do" type="radio" value="included" />
              <h4>Not watching</h4>
              <p>You will only receive notifications when you participate or are mentioned.</p>
            </label>
            <span class="context-button-text js-context-button-text">
              <span class="mini-icon mini-icon-watching"></span>
              Watch
            </span>
          </li>
          <li class="selector-item js-navigation-item js-navigation-target ">
            <span class="mini-icon mini-icon-confirm"></span>
            <label>
              <input id="do_subscribed" name="do" type="radio" value="subscribed" />
              <h4>Watching</h4>
              <p>You will receive all notifications for this repository.</p>
            </label>
            <span class="context-button-text js-context-button-text">
              <span class="mini-icon mini-icon-unwatch"></span>
              Unwatch
            </span>
          </li>
          <li class="selector-item js-navigation-item js-navigation-target ">
            <span class="mini-icon mini-icon-confirm"></span>
            <label>
              <input id="do_ignore" name="do" type="radio" value="ignore" />
              <h4>Ignored</h4>
              <p>You will not receive notifications for this repository.</p>
            </label>
            <span class="context-button-text js-context-button-text">
              <span class="mini-icon mini-icon-mute"></span>
              Stop ignoring
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</form>
          </li>

          <li class="js-toggler-container js-social-container starring-container ">
            <a href="/micramm/HaeffnerLabLattice/unstar" class="minibutton js-toggler-target starred" data-remote="true" data-method="post" rel="nofollow">
              <span class="mini-icon mini-icon-star"></span>Unstar
            </a><a href="/micramm/HaeffnerLabLattice/star" class="minibutton js-toggler-target unstarred" data-remote="true" data-method="post" rel="nofollow">
              <span class="mini-icon mini-icon-star"></span>Star
            </a><a class="social-count js-social-count" href="/micramm/HaeffnerLabLattice/stargazers">3</a>
          </li>

              <li><a href="/micramm/HaeffnerLabLattice/fork" class="minibutton js-toggler-target fork-button lighter" rel="nofollow" data-method="post"><span class="mini-icon mini-icon-fork"></span>Fork</a><a href="/micramm/HaeffnerLabLattice/network" class="social-count">0</a>
              </li>


    </ul>

          <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
            <span class="repo-label"><span>public</span></span>
            <span class="mega-icon mega-icon-public-repo"></span>
            <span class="author vcard">
              <a href="/micramm" class="url fn" itemprop="url" rel="author">
              <span itemprop="title">micramm</span>
              </a></span> /
            <strong><a href="/micramm/HaeffnerLabLattice" class="js-current-repository">HaeffnerLabLattice</a></strong>
          </h1>
        </div>

          

  <ul class="tabs">
    <li><a href="/micramm/HaeffnerLabLattice" class="selected" highlight="repo_sourcerepo_downloadsrepo_commitsrepo_tagsrepo_branches">Code</a></li>
    <li><a href="/micramm/HaeffnerLabLattice/network" highlight="repo_network">Network</a></li>
    <li><a href="/micramm/HaeffnerLabLattice/pulls" highlight="repo_pulls">Pull Requests <span class='counter'>0</span></a></li>


      <li><a href="/micramm/HaeffnerLabLattice/wiki" highlight="repo_wiki">Wiki</a></li>


    <li><a href="/micramm/HaeffnerLabLattice/graphs" highlight="repo_graphsrepo_contributors">Graphs</a></li>


  </ul>
  
<div class="frame frame-center tree-finder" style="display:none"
      data-tree-list-url="/micramm/HaeffnerLabLattice/tree-list/0549a77bdb10ed62f3f0be14f802e7f8f184930a"
      data-blob-url-prefix="/micramm/HaeffnerLabLattice/blob/0549a77bdb10ed62f3f0be14f802e7f8f184930a"
    >

  <div class="breadcrumb">
    <span class="bold"><a href="/micramm/HaeffnerLabLattice">HaeffnerLabLattice</a></span> /
    <input class="tree-finder-input js-navigation-enable" type="text" name="query" autocomplete="off" spellcheck="false">
  </div>

    <div class="octotip">
      <p>
        <a href="/micramm/HaeffnerLabLattice/dismiss-tree-finder-help" class="dismiss js-dismiss-tree-list-help" title="Hide this notice forever" rel="nofollow">Dismiss</a>
        <span class="bold">Octotip:</span> You've activated the <em>file finder</em>
        by pressing <span class="kbd">t</span> Start typing to filter the
        file list. Use <span class="kbd badmono">↑</span> and
        <span class="kbd badmono">↓</span> to navigate,
        <span class="kbd">enter</span> to view files.
      </p>
    </div>

  <table class="tree-browser" cellpadding="0" cellspacing="0">
    <tr class="js-header"><th>&nbsp;</th><th>name</th></tr>
    <tr class="js-no-results no-results" style="display: none">
      <th colspan="2">No matching files</th>
    </tr>
    <tbody class="js-results-list js-navigation-container">
    </tbody>
  </table>
</div>

<div id="jump-to-line" style="display:none">
  <h2>Jump to Line</h2>
  <form accept-charset="UTF-8">
    <input class="textfield" type="text">
    <div class="full-button">
      <button type="submit" class="classy">
        Go
      </button>
    </div>
  </form>
</div>


<div class="tabnav">

  <span class="tabnav-right">
    <ul class="tabnav-tabs">
      <li><a href="/micramm/HaeffnerLabLattice/tags" class="tabnav-tab" highlight="repo_tags">Tags <span class="counter blank">0</span></a></li>
      <li><a href="/micramm/HaeffnerLabLattice/downloads" class="tabnav-tab" highlight="repo_downloads">Downloads <span class="counter blank">0</span></a></li>
    </ul>
    
  </span>

  <div class="tabnav-widget scope">

    <div class="context-menu-container js-menu-container js-context-menu">
      <a href="#"
         class="minibutton bigger switcher js-menu-target js-commitish-button btn-branch repo-tree"
         data-hotkey="w"
         data-master-branch="master"
         data-ref="master">
         <span><em class="mini-icon mini-icon-branch"></em><i>branch:</i> master</span>
      </a>

      <div class="context-pane commitish-context js-menu-content">
        <a href="javascript:;" class="close js-menu-close"><span class="mini-icon mini-icon-remove-close"></span></a>
        <div class="context-title">Switch branches/tags</div>
        <div class="context-body pane-selector commitish-selector js-navigation-container">
          <div class="filterbar">
            <input type="text" id="context-commitish-filter-field" class="js-navigation-enable" placeholder="Filter branches/tags" data-filterable />
            <ul class="tabs">
              <li><a href="#" data-filter="branches" class="selected">Branches</a></li>
              <li><a href="#" data-filter="tags">Tags</a></li>
            </ul>
          </div>

          <div class="js-filter-tab js-filter-branches" data-filterable-for="context-commitish-filter-field" data-filterable-type=substring>
            <div class="no-results js-not-filterable">Nothing to show</div>
              <div class="commitish-item branch-commitish selector-item js-navigation-item js-navigation-target selected">
                <span class="mini-icon mini-icon-confirm"></span>
                <h4>
                    <a href="/micramm/HaeffnerLabLattice/blob/master/lattice/cdllservers/APTMotor/APTMotorServer.py" class="js-navigation-open" data-name="master" rel="nofollow">master</a>
                </h4>
              </div>
          </div>

          <div class="js-filter-tab js-filter-tags" style="display:none" data-filterable-for="context-commitish-filter-field" data-filterable-type=substring>
            <div class="no-results js-not-filterable">Nothing to show</div>
          </div>
        </div>
      </div><!-- /.commitish-context-context -->
    </div>
  </div> <!-- /.scope -->

  <ul class="tabnav-tabs">
    <li><a href="/micramm/HaeffnerLabLattice" class="selected tabnav-tab" highlight="repo_source">Files</a></li>
    <li><a href="/micramm/HaeffnerLabLattice/commits/master" class="tabnav-tab" highlight="repo_commits">Commits</a></li>
    <li><a href="/micramm/HaeffnerLabLattice/branches" class="tabnav-tab" highlight="repo_branches" rel="nofollow">Branches <span class="counter ">1</span></a></li>
  </ul>

</div>

  
  
  


          

        </div><!-- /.repohead -->

        <div id="js-repo-pjax-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:7a5dd9f50b3e36c7ec6f2be9dc82bc6f -->
<!-- blob contrib frag key: views10/v8/blob_contributors:v21:7a5dd9f50b3e36c7ec6f2be9dc82bc6f -->

<!-- block_view_fragment_key: views10/v8/blob:v21:100c86d5cfff08854dbedf00a44baaba -->

  <div id="slider">

    <div class="breadcrumb" data-path="lattice/cdllservers/APTMotor/APTMotorServer.py/">
      <b itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/micramm/HaeffnerLabLattice/tree/29e6162b040e4944875e10f3965656663f53ef2d" class="js-rewrite-sha" itemprop="url"><span itemprop="title">HaeffnerLabLattice</span></a></b> / <span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/micramm/HaeffnerLabLattice/tree/29e6162b040e4944875e10f3965656663f53ef2d/lattice" class="js-rewrite-sha" itemscope="url"><span itemprop="title">lattice</span></a></span> / <span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/micramm/HaeffnerLabLattice/tree/29e6162b040e4944875e10f3965656663f53ef2d/lattice/cdllservers" class="js-rewrite-sha" itemscope="url"><span itemprop="title">cdllservers</span></a></span> / <span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/micramm/HaeffnerLabLattice/tree/29e6162b040e4944875e10f3965656663f53ef2d/lattice/cdllservers/APTMotor" class="js-rewrite-sha" itemscope="url"><span itemprop="title">APTMotor</span></a></span> / <strong class="final-path">APTMotorServer.py</strong> <span class="js-clippy mini-icon mini-icon-clippy " data-clipboard-text="lattice/cdllservers/APTMotor/APTMotorServer.py" data-copied-hint="copied!" data-copy-hint="copy to clipboard"></span>
    </div>

      
  <div class="commit file-history-tease js-blob-contributors-content" data-path="lattice/cdllservers/APTMotor/APTMotorServer.py/">
    <img class="main-avatar" height="24" src="https://secure.gravatar.com/avatar/b817c6e01456b5f20c0644b056c2cc76?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="24" />
    <span class="author"><a href="/Hlab">Hlab</a></span>
    <time class="js-relative-date" datetime="2012-07-09T14:20:16-07:00" title="2012-07-09 14:20:16">July 09, 2012</time>
    <div class="commit-title">
        <a href="/micramm/HaeffnerLabLattice/commit/e175b0f9f8ed580bcb6e41259eba4a7ea15d7bcb" class="message">Ion Swap client analyzes old datsets and shows camera images.</a>
    </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>2</strong> contributors</a></p>
          <a class="avatar tooltipped downwards" title="micramm" href="/micramm/HaeffnerLabLattice/commits/master/lattice/cdllservers/APTMotor/APTMotorServer.py?author=micramm"><img height="20" src="https://secure.gravatar.com/avatar/be7d1dce901817f9f5505eb9b1536782?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="20" /></a>
    <a class="avatar tooltipped downwards" title="Hlab" href="/micramm/HaeffnerLabLattice/commits/master/lattice/cdllservers/APTMotor/APTMotorServer.py?author=Hlab"><img height="20" src="https://secure.gravatar.com/avatar/b817c6e01456b5f20c0644b056c2cc76?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="20" /></a>


    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2>Users on GitHub who have contributed to this file</h2>
      <ul class="facebox-user-list">
        <li>
          <img height="24" src="https://secure.gravatar.com/avatar/be7d1dce901817f9f5505eb9b1536782?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="24" />
          <a href="/micramm">micramm</a>
        </li>
        <li>
          <img height="24" src="https://secure.gravatar.com/avatar/b817c6e01456b5f20c0644b056c2cc76?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="24" />
          <a href="/Hlab">Hlab</a>
        </li>
      </ul>
    </div>
  </div>


    <div class="frames">
      <div class="frame frame-center" data-path="lattice/cdllservers/APTMotor/APTMotorServer.py/" data-permalink-url="/micramm/HaeffnerLabLattice/blob/29e6162b040e4944875e10f3965656663f53ef2d/lattice/cdllservers/APTMotor/APTMotorServer.py" data-title="HaeffnerLabLattice/lattice/cdllservers/APTMotor/APTMotorServer.py at master · micramm/HaeffnerLabLattice · GitHub" data-type="blob">

        <div id="files" class="bubble">
          <div class="file">
            <div class="meta">
              <div class="info">
                <span class="icon"><b class="mini-icon mini-icon-text-file"></b></span>
                <span class="mode" title="File Mode">file</span>
                  <span>309 lines (264 sloc)</span>
                <span>13.226 kb</span>
              </div>
              <ul class="button-group actions">
                  <li>
                    <a class="grouped-button file-edit-link minibutton bigger lighter js-rewrite-sha" href="/micramm/HaeffnerLabLattice/edit/29e6162b040e4944875e10f3965656663f53ef2d/lattice/cdllservers/APTMotor/APTMotorServer.py" data-method="post" rel="nofollow" data-hotkey="e">Edit</a>
                  </li>
                <li>
                  <a href="/micramm/HaeffnerLabLattice/raw/master/lattice/cdllservers/APTMotor/APTMotorServer.py" class="minibutton grouped-button bigger lighter" id="raw-url">Raw</a>
                </li>
                  <li>
                    <a href="/micramm/HaeffnerLabLattice/blame/master/lattice/cdllservers/APTMotor/APTMotorServer.py" class="minibutton grouped-button bigger lighter">Blame</a>
                  </li>
                <li>
                  <a href="/micramm/HaeffnerLabLattice/commits/master/lattice/cdllservers/APTMotor/APTMotorServer.py" class="minibutton grouped-button bigger lighter" rel="nofollow">History</a>
                </li>
              </ul>
            </div>
              <div class="data type-python">
      <table cellpadding="0" cellspacing="0" class="lines">
        <tr>
          <td>
            <pre class="line_numbers"><span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>
<span id="L101" rel="#L101">101</span>
<span id="L102" rel="#L102">102</span>
<span id="L103" rel="#L103">103</span>
<span id="L104" rel="#L104">104</span>
<span id="L105" rel="#L105">105</span>
<span id="L106" rel="#L106">106</span>
<span id="L107" rel="#L107">107</span>
<span id="L108" rel="#L108">108</span>
<span id="L109" rel="#L109">109</span>
<span id="L110" rel="#L110">110</span>
<span id="L111" rel="#L111">111</span>
<span id="L112" rel="#L112">112</span>
<span id="L113" rel="#L113">113</span>
<span id="L114" rel="#L114">114</span>
<span id="L115" rel="#L115">115</span>
<span id="L116" rel="#L116">116</span>
<span id="L117" rel="#L117">117</span>
<span id="L118" rel="#L118">118</span>
<span id="L119" rel="#L119">119</span>
<span id="L120" rel="#L120">120</span>
<span id="L121" rel="#L121">121</span>
<span id="L122" rel="#L122">122</span>
<span id="L123" rel="#L123">123</span>
<span id="L124" rel="#L124">124</span>
<span id="L125" rel="#L125">125</span>
<span id="L126" rel="#L126">126</span>
<span id="L127" rel="#L127">127</span>
<span id="L128" rel="#L128">128</span>
<span id="L129" rel="#L129">129</span>
<span id="L130" rel="#L130">130</span>
<span id="L131" rel="#L131">131</span>
<span id="L132" rel="#L132">132</span>
<span id="L133" rel="#L133">133</span>
<span id="L134" rel="#L134">134</span>
<span id="L135" rel="#L135">135</span>
<span id="L136" rel="#L136">136</span>
<span id="L137" rel="#L137">137</span>
<span id="L138" rel="#L138">138</span>
<span id="L139" rel="#L139">139</span>
<span id="L140" rel="#L140">140</span>
<span id="L141" rel="#L141">141</span>
<span id="L142" rel="#L142">142</span>
<span id="L143" rel="#L143">143</span>
<span id="L144" rel="#L144">144</span>
<span id="L145" rel="#L145">145</span>
<span id="L146" rel="#L146">146</span>
<span id="L147" rel="#L147">147</span>
<span id="L148" rel="#L148">148</span>
<span id="L149" rel="#L149">149</span>
<span id="L150" rel="#L150">150</span>
<span id="L151" rel="#L151">151</span>
<span id="L152" rel="#L152">152</span>
<span id="L153" rel="#L153">153</span>
<span id="L154" rel="#L154">154</span>
<span id="L155" rel="#L155">155</span>
<span id="L156" rel="#L156">156</span>
<span id="L157" rel="#L157">157</span>
<span id="L158" rel="#L158">158</span>
<span id="L159" rel="#L159">159</span>
<span id="L160" rel="#L160">160</span>
<span id="L161" rel="#L161">161</span>
<span id="L162" rel="#L162">162</span>
<span id="L163" rel="#L163">163</span>
<span id="L164" rel="#L164">164</span>
<span id="L165" rel="#L165">165</span>
<span id="L166" rel="#L166">166</span>
<span id="L167" rel="#L167">167</span>
<span id="L168" rel="#L168">168</span>
<span id="L169" rel="#L169">169</span>
<span id="L170" rel="#L170">170</span>
<span id="L171" rel="#L171">171</span>
<span id="L172" rel="#L172">172</span>
<span id="L173" rel="#L173">173</span>
<span id="L174" rel="#L174">174</span>
<span id="L175" rel="#L175">175</span>
<span id="L176" rel="#L176">176</span>
<span id="L177" rel="#L177">177</span>
<span id="L178" rel="#L178">178</span>
<span id="L179" rel="#L179">179</span>
<span id="L180" rel="#L180">180</span>
<span id="L181" rel="#L181">181</span>
<span id="L182" rel="#L182">182</span>
<span id="L183" rel="#L183">183</span>
<span id="L184" rel="#L184">184</span>
<span id="L185" rel="#L185">185</span>
<span id="L186" rel="#L186">186</span>
<span id="L187" rel="#L187">187</span>
<span id="L188" rel="#L188">188</span>
<span id="L189" rel="#L189">189</span>
<span id="L190" rel="#L190">190</span>
<span id="L191" rel="#L191">191</span>
<span id="L192" rel="#L192">192</span>
<span id="L193" rel="#L193">193</span>
<span id="L194" rel="#L194">194</span>
<span id="L195" rel="#L195">195</span>
<span id="L196" rel="#L196">196</span>
<span id="L197" rel="#L197">197</span>
<span id="L198" rel="#L198">198</span>
<span id="L199" rel="#L199">199</span>
<span id="L200" rel="#L200">200</span>
<span id="L201" rel="#L201">201</span>
<span id="L202" rel="#L202">202</span>
<span id="L203" rel="#L203">203</span>
<span id="L204" rel="#L204">204</span>
<span id="L205" rel="#L205">205</span>
<span id="L206" rel="#L206">206</span>
<span id="L207" rel="#L207">207</span>
<span id="L208" rel="#L208">208</span>
<span id="L209" rel="#L209">209</span>
<span id="L210" rel="#L210">210</span>
<span id="L211" rel="#L211">211</span>
<span id="L212" rel="#L212">212</span>
<span id="L213" rel="#L213">213</span>
<span id="L214" rel="#L214">214</span>
<span id="L215" rel="#L215">215</span>
<span id="L216" rel="#L216">216</span>
<span id="L217" rel="#L217">217</span>
<span id="L218" rel="#L218">218</span>
<span id="L219" rel="#L219">219</span>
<span id="L220" rel="#L220">220</span>
<span id="L221" rel="#L221">221</span>
<span id="L222" rel="#L222">222</span>
<span id="L223" rel="#L223">223</span>
<span id="L224" rel="#L224">224</span>
<span id="L225" rel="#L225">225</span>
<span id="L226" rel="#L226">226</span>
<span id="L227" rel="#L227">227</span>
<span id="L228" rel="#L228">228</span>
<span id="L229" rel="#L229">229</span>
<span id="L230" rel="#L230">230</span>
<span id="L231" rel="#L231">231</span>
<span id="L232" rel="#L232">232</span>
<span id="L233" rel="#L233">233</span>
<span id="L234" rel="#L234">234</span>
<span id="L235" rel="#L235">235</span>
<span id="L236" rel="#L236">236</span>
<span id="L237" rel="#L237">237</span>
<span id="L238" rel="#L238">238</span>
<span id="L239" rel="#L239">239</span>
<span id="L240" rel="#L240">240</span>
<span id="L241" rel="#L241">241</span>
<span id="L242" rel="#L242">242</span>
<span id="L243" rel="#L243">243</span>
<span id="L244" rel="#L244">244</span>
<span id="L245" rel="#L245">245</span>
<span id="L246" rel="#L246">246</span>
<span id="L247" rel="#L247">247</span>
<span id="L248" rel="#L248">248</span>
<span id="L249" rel="#L249">249</span>
<span id="L250" rel="#L250">250</span>
<span id="L251" rel="#L251">251</span>
<span id="L252" rel="#L252">252</span>
<span id="L253" rel="#L253">253</span>
<span id="L254" rel="#L254">254</span>
<span id="L255" rel="#L255">255</span>
<span id="L256" rel="#L256">256</span>
<span id="L257" rel="#L257">257</span>
<span id="L258" rel="#L258">258</span>
<span id="L259" rel="#L259">259</span>
<span id="L260" rel="#L260">260</span>
<span id="L261" rel="#L261">261</span>
<span id="L262" rel="#L262">262</span>
<span id="L263" rel="#L263">263</span>
<span id="L264" rel="#L264">264</span>
<span id="L265" rel="#L265">265</span>
<span id="L266" rel="#L266">266</span>
<span id="L267" rel="#L267">267</span>
<span id="L268" rel="#L268">268</span>
<span id="L269" rel="#L269">269</span>
<span id="L270" rel="#L270">270</span>
<span id="L271" rel="#L271">271</span>
<span id="L272" rel="#L272">272</span>
<span id="L273" rel="#L273">273</span>
<span id="L274" rel="#L274">274</span>
<span id="L275" rel="#L275">275</span>
<span id="L276" rel="#L276">276</span>
<span id="L277" rel="#L277">277</span>
<span id="L278" rel="#L278">278</span>
<span id="L279" rel="#L279">279</span>
<span id="L280" rel="#L280">280</span>
<span id="L281" rel="#L281">281</span>
<span id="L282" rel="#L282">282</span>
<span id="L283" rel="#L283">283</span>
<span id="L284" rel="#L284">284</span>
<span id="L285" rel="#L285">285</span>
<span id="L286" rel="#L286">286</span>
<span id="L287" rel="#L287">287</span>
<span id="L288" rel="#L288">288</span>
<span id="L289" rel="#L289">289</span>
<span id="L290" rel="#L290">290</span>
<span id="L291" rel="#L291">291</span>
<span id="L292" rel="#L292">292</span>
<span id="L293" rel="#L293">293</span>
<span id="L294" rel="#L294">294</span>
<span id="L295" rel="#L295">295</span>
<span id="L296" rel="#L296">296</span>
<span id="L297" rel="#L297">297</span>
<span id="L298" rel="#L298">298</span>
<span id="L299" rel="#L299">299</span>
<span id="L300" rel="#L300">300</span>
<span id="L301" rel="#L301">301</span>
<span id="L302" rel="#L302">302</span>
<span id="L303" rel="#L303">303</span>
<span id="L304" rel="#L304">304</span>
<span id="L305" rel="#L305">305</span>
<span id="L306" rel="#L306">306</span>
<span id="L307" rel="#L307">307</span>
<span id="L308" rel="#L308">308</span>
<span id="L309" rel="#L309">309</span>
</pre>
          </td>
          <td width="100%">
                <div class="highlight"><pre><div class='line' id='LC1'><span class="kn">from</span> <span class="nn">labrad.server</span> <span class="kn">import</span> <span class="n">LabradServer</span><span class="p">,</span> <span class="n">setting</span><span class="p">,</span> <span class="n">Signal</span></div><div class='line' id='LC2'><span class="kn">from</span> <span class="nn">twisted.internet.defer</span> <span class="kn">import</span> <span class="n">inlineCallbacks</span><span class="p">,</span> <span class="n">returnValue</span></div><div class='line' id='LC3'><span class="kn">from</span> <span class="nn">twisted.internet.threads</span> <span class="kn">import</span> <span class="n">deferToThread</span></div><div class='line' id='LC4'><span class="kn">from</span> <span class="nn">ctypes</span> <span class="kn">import</span> <span class="n">c_long</span><span class="p">,</span> <span class="n">c_buffer</span><span class="p">,</span> <span class="n">c_float</span><span class="p">,</span> <span class="n">windll</span><span class="p">,</span> <span class="n">pointer</span></div><div class='line' id='LC5'><br/></div><div class='line' id='LC6'><span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC7'><span class="sd">### BEGIN NODE INFO</span></div><div class='line' id='LC8'><span class="sd">[info]</span></div><div class='line' id='LC9'><span class="sd">name =  APT Motor Server</span></div><div class='line' id='LC10'><span class="sd">version = 1.0</span></div><div class='line' id='LC11'><span class="sd">description = </span></div><div class='line' id='LC12'><br/></div><div class='line' id='LC13'><span class="sd">[startup]</span></div><div class='line' id='LC14'><span class="sd">cmdline = %PYTHON% %FILE%</span></div><div class='line' id='LC15'><span class="sd">timeout = 20</span></div><div class='line' id='LC16'><br/></div><div class='line' id='LC17'><span class="sd">[shutdown]</span></div><div class='line' id='LC18'><span class="sd">message = 987654321</span></div><div class='line' id='LC19'><span class="sd">timeout = 5</span></div><div class='line' id='LC20'><span class="sd">### END NODE INFO</span></div><div class='line' id='LC21'><span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC22'><br/></div><div class='line' id='LC23'><span class="k">class</span> <span class="nc">APTMotor</span><span class="p">():</span></div><div class='line' id='LC24'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></div><div class='line' id='LC25'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span> <span class="o">=</span> <span class="n">windll</span><span class="o">.</span><span class="n">LoadLibrary</span><span class="p">(</span><span class="s">&quot;APT.dll&quot;</span><span class="p">)</span></div><div class='line' id='LC26'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c">#self.aptdll.EnableEventDlg(False)</span></div><div class='line' id='LC27'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">APTInit</span><span class="p">()</span></div><div class='line' id='LC28'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">print</span> <span class="s">&#39;APT initialized&#39;</span></div><div class='line' id='LC29'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">HWType</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="mi">31</span><span class="p">)</span> <span class="c"># 31 means TDC001 controller</span></div><div class='line' id='LC30'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC31'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getNumberOfHardwareUnits</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></div><div class='line' id='LC32'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">numUnits</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">()</span></div><div class='line' id='LC33'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">GetNumHWUnitsEx</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">HWType</span><span class="p">,</span> <span class="n">pointer</span><span class="p">(</span><span class="n">numUnits</span><span class="p">))</span></div><div class='line' id='LC34'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">numUnits</span><span class="o">.</span><span class="n">value</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC36'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getSerialNumber</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">index</span><span class="p">):</span></div><div class='line' id='LC37'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">()</span></div><div class='line' id='LC38'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">hardwareIndex</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">index</span><span class="p">)</span></div><div class='line' id='LC39'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">GetHWSerialNumEx</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">HWType</span><span class="p">,</span> <span class="n">hardwareIndex</span><span class="p">,</span> <span class="n">pointer</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">))</span></div><div class='line' id='LC40'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">HWSerialNum</span><span class="o">.</span><span class="n">value</span></div><div class='line' id='LC41'><br/></div><div class='line' id='LC42'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">initializeHardwareDevice</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC43'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC44'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">InitHWDevice</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">)</span></div><div class='line' id='LC45'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># need some kind of error reporting here</span></div><div class='line' id='LC46'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">True</span></div><div class='line' id='LC47'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC48'><span class="c">#    @inlineCallbacks</span></div><div class='line' id='LC49'><span class="c">#    def initializeHardwareDevice(self, serialNumber):</span></div><div class='line' id='LC50'><span class="c">#        print serialNumber</span></div><div class='line' id='LC51'><span class="c">#        HWSerialNum = c_long(serialNumber)</span></div><div class='line' id='LC52'><span class="c">#        yield self.aptdll.InitHWDevice(HWSerialNum)</span></div><div class='line' id='LC53'><span class="c">#        # need some kind of error reporting here</span></div><div class='line' id='LC54'><span class="c">#        returnValue( True )</span></div><div class='line' id='LC55'><span class="c">#        </span></div><div class='line' id='LC56'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getHardwareInformation</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC57'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">model</span> <span class="o">=</span> <span class="n">c_buffer</span><span class="p">(</span><span class="mi">255</span><span class="p">)</span></div><div class='line' id='LC59'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">softwareVersion</span> <span class="o">=</span> <span class="n">c_buffer</span><span class="p">(</span><span class="mi">255</span><span class="p">)</span></div><div class='line' id='LC60'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">hardwareNotes</span> <span class="o">=</span> <span class="n">c_buffer</span><span class="p">(</span><span class="mi">255</span><span class="p">)</span></div><div class='line' id='LC61'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">GetHWInfo</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">model</span><span class="p">,</span> <span class="mi">255</span><span class="p">,</span> <span class="n">softwareVersion</span><span class="p">,</span> <span class="mi">255</span><span class="p">,</span> <span class="n">hardwareNotes</span><span class="p">,</span> <span class="mi">255</span><span class="p">)</span>      </div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">hwinfo</span> <span class="o">=</span> <span class="p">[</span><span class="n">model</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">softwareVersion</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">hardwareNotes</span><span class="o">.</span><span class="n">value</span><span class="p">]</span></div><div class='line' id='LC63'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">hwinfo</span></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC65'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getStageAxisInformation</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC66'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC67'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">minimumPosition</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC68'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">maximumPosition</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC69'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">units</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">()</span></div><div class='line' id='LC70'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pitch</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC71'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_GetStageAxisInfo</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">pointer</span><span class="p">(</span><span class="n">minimumPosition</span><span class="p">),</span> <span class="n">pointer</span><span class="p">(</span><span class="n">maximumPosition</span><span class="p">),</span> <span class="n">pointer</span><span class="p">(</span><span class="n">units</span><span class="p">),</span> <span class="n">pointer</span><span class="p">(</span><span class="n">pitch</span><span class="p">))</span></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">stageAxisInformation</span> <span class="o">=</span> <span class="p">[</span><span class="n">minimumPosition</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">maximumPosition</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">units</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">pitch</span><span class="o">.</span><span class="n">value</span><span class="p">]</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">stageAxisInformation</span></div><div class='line' id='LC74'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC75'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">setStageAxisInformation</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">,</span> <span class="n">minimumPosition</span><span class="p">,</span> <span class="n">maximumPosition</span><span class="p">):</span></div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC77'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">minimumPosition</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">minimumPosition</span><span class="p">)</span></div><div class='line' id='LC78'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">maximumPosition</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">maximumPosition</span><span class="p">)</span></div><div class='line' id='LC79'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">units</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span> <span class="c">#units of mm</span></div><div class='line' id='LC80'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pitch</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="o">.</span><span class="mi">5</span><span class="p">)</span> <span class="c">#standard pitch</span></div><div class='line' id='LC81'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_SetStageAxisInfo</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">minimumPosition</span><span class="p">,</span> <span class="n">maximumPosition</span><span class="p">,</span> <span class="n">units</span><span class="p">,</span> <span class="n">pitch</span><span class="p">)</span></div><div class='line' id='LC82'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">True</span></div><div class='line' id='LC83'><br/></div><div class='line' id='LC84'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC85'><span class="c">#    def getHardwareLimitSwitches(self, serialNumber):</span></div><div class='line' id='LC86'><span class="c">#        HWSerialNum = c_long(serialNumber)</span></div><div class='line' id='LC87'><span class="c">#        reverseLimitSwitch = c_long()</span></div><div class='line' id='LC88'><span class="c">#        forwardLimitSwitch = c_long()</span></div><div class='line' id='LC89'><span class="c">#        self.aptdll.MOT_GetHWLimSwitches(HWSerialNum, pointer(reverseLimitSwitch), pointer(forwardLimitSwitch))</span></div><div class='line' id='LC90'><span class="c">#        hardwareLimitSwitches = [reverseLimitSwitch.value, forwardLimitSwitch.value]</span></div><div class='line' id='LC91'><span class="c">#        return hardwareLimitSwitches</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getVelocityParameters</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC94'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC95'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">minimumVelocity</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC96'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">acceleration</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC97'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">maximumVelocity</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC98'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_GetVelParams</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">pointer</span><span class="p">(</span><span class="n">minimumVelocity</span><span class="p">),</span> <span class="n">pointer</span><span class="p">(</span><span class="n">acceleration</span><span class="p">),</span> <span class="n">pointer</span><span class="p">(</span><span class="n">maximumVelocity</span><span class="p">))</span></div><div class='line' id='LC99'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">velocityParameters</span> <span class="o">=</span> <span class="p">[</span><span class="n">minimumVelocity</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">acceleration</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">maximumVelocity</span><span class="o">.</span><span class="n">value</span><span class="p">]</span></div><div class='line' id='LC100'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">velocityParameters</span></div><div class='line' id='LC101'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC102'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">setVelocityParameters</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">,</span> <span class="n">minVel</span><span class="p">,</span> <span class="n">acc</span><span class="p">,</span> <span class="n">maxVel</span><span class="p">):</span></div><div class='line' id='LC103'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC104'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">minimumVelocity</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">minVel</span><span class="p">)</span></div><div class='line' id='LC105'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">acceleration</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">acc</span><span class="p">)</span></div><div class='line' id='LC106'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">maximumVelocity</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">maxVel</span><span class="p">)</span></div><div class='line' id='LC107'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_SetVelParams</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">minimumVelocity</span><span class="p">,</span> <span class="n">acceleration</span><span class="p">,</span> <span class="n">maximumVelocity</span><span class="p">)</span></div><div class='line' id='LC108'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">True</span></div><div class='line' id='LC109'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC110'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getVelocityParameterLimits</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC111'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC112'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">maximumAcceleration</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC113'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">maximumVelocity</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC114'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_GetVelParamLimits</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">pointer</span><span class="p">(</span><span class="n">maximumAcceleration</span><span class="p">),</span> <span class="n">pointer</span><span class="p">(</span><span class="n">maximumVelocity</span><span class="p">))</span></div><div class='line' id='LC115'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">velocityParameterLimits</span> <span class="o">=</span> <span class="p">[</span><span class="n">maximumAcceleration</span><span class="o">.</span><span class="n">value</span><span class="p">,</span> <span class="n">maximumVelocity</span><span class="o">.</span><span class="n">value</span><span class="p">]</span></div><div class='line' id='LC116'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">velocityParameterLimits</span>  </div><div class='line' id='LC117'><br/></div><div class='line' id='LC118'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getPosition</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC119'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC120'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">position</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">()</span></div><div class='line' id='LC121'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_GetPosition</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">pointer</span><span class="p">(</span><span class="n">position</span><span class="p">))</span></div><div class='line' id='LC122'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">position</span><span class="o">.</span><span class="n">value</span>    </div><div class='line' id='LC123'><br/></div><div class='line' id='LC124'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">moveRelative</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">,</span> <span class="n">relDistance</span><span class="p">):</span></div><div class='line' id='LC125'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC126'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">relativeDistance</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">relDistance</span><span class="p">)</span></div><div class='line' id='LC127'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_MoveRelativeEx</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">relativeDistance</span><span class="p">,</span> <span class="bp">True</span><span class="p">)</span></div><div class='line' id='LC128'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">True</span></div><div class='line' id='LC129'><br/></div><div class='line' id='LC130'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">moveAbsolute</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">,</span> <span class="n">absPosition</span><span class="p">):</span></div><div class='line' id='LC131'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC132'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">absolutePosition</span> <span class="o">=</span> <span class="n">c_float</span><span class="p">(</span><span class="n">absPosition</span><span class="p">)</span></div><div class='line' id='LC133'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_MoveAbsoluteEx</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">,</span> <span class="n">absolutePosition</span><span class="p">,</span> <span class="bp">True</span><span class="p">)</span></div><div class='line' id='LC134'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">True</span></div><div class='line' id='LC135'><br/></div><div class='line' id='LC136'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">identify</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">serialNumber</span><span class="p">):</span></div><div class='line' id='LC137'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">HWSerialNum</span> <span class="o">=</span> <span class="n">c_long</span><span class="p">(</span><span class="n">serialNumber</span><span class="p">)</span></div><div class='line' id='LC138'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">MOT_Identify</span><span class="p">(</span><span class="n">HWSerialNum</span><span class="p">)</span></div><div class='line' id='LC139'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">True</span></div><div class='line' id='LC140'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC141'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">cleanUpAPT</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></div><div class='line' id='LC142'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptdll</span><span class="o">.</span><span class="n">APTCleanUp</span><span class="p">()</span></div><div class='line' id='LC143'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">print</span> <span class="s">&#39;APT cleaned up&#39;</span>  </div><div class='line' id='LC144'><br/></div><div class='line' id='LC145'><span class="k">class</span> <span class="nc">stage</span><span class="p">():</span></div><div class='line' id='LC146'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">serial</span><span class="p">,</span> <span class="n">initialized</span><span class="o">=</span><span class="bp">False</span><span class="p">):</span></div><div class='line' id='LC147'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">name</span></div><div class='line' id='LC148'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">serial</span> <span class="o">=</span> <span class="n">serial</span></div><div class='line' id='LC149'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">initialized</span> <span class="o">=</span> <span class="n">initialized</span></div><div class='line' id='LC150'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">minpos</span> <span class="o">=</span> <span class="o">-</span><span class="mf">6.5</span></div><div class='line' id='LC151'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">maxpos</span> <span class="o">=</span> <span class="mf">6.5</span></div><div class='line' id='LC152'><br/></div><div class='line' id='LC153'><span class="k">class</span> <span class="nc">APTMotorServer</span><span class="p">(</span><span class="n">LabradServer</span><span class="p">):</span></div><div class='line' id='LC154'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot; Contains methods that interact with the APT motor controller &quot;&quot;&quot;</span></div><div class='line' id='LC155'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC156'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">name</span> <span class="o">=</span> <span class="s">&quot;APT Motor Server&quot;</span></div><div class='line' id='LC157'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC158'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">onVelocityParameterChange</span> <span class="o">=</span> <span class="n">Signal</span><span class="p">(</span><span class="mi">111111</span><span class="p">,</span> <span class="s">&#39;signal: velocity parameter change&#39;</span><span class="p">,</span> <span class="s">&#39;w&#39;</span><span class="p">)</span></div><div class='line' id='LC159'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">onPositionChange</span> <span class="o">=</span> <span class="n">Signal</span><span class="p">(</span><span class="mi">222222</span><span class="p">,</span> <span class="s">&#39;signal: position change&#39;</span><span class="p">,</span> <span class="s">&#39;w&#39;</span><span class="p">)</span></div><div class='line' id='LC160'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC161'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># Device Dictionary, assigning meaningful names to serial numbers</span></div><div class='line' id='LC162'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">initServer</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></div><div class='line' id='LC163'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">deviceDict</span> <span class="o">=</span> <span class="p">{</span><span class="s">&#39;Axial LR&#39;</span><span class="p">:</span> <span class="n">stage</span><span class="p">(</span><span class="s">&#39;Axial LR&#39;</span><span class="p">,</span> <span class="mi">83825962</span><span class="p">),</span></div><div class='line' id='LC164'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Axial UD&#39;</span><span class="p">:</span> <span class="n">stage</span><span class="p">(</span><span class="s">&#39;Axial UD&#39;</span><span class="p">,</span><span class="mi">83815664</span><span class="p">),</span></div><div class='line' id='LC165'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC166'><span class="c">#                       &#39;Radial FB&#39;: 83825936,</span></div><div class='line' id='LC167'><span class="c">#                       &#39;Axial LR&#39;: 63001773,</span></div><div class='line' id='LC168'><span class="c">#                       &#39;Auxilliary&#39;: 83816548,</span></div><div class='line' id='LC169'><span class="c">#                       &#39;Simulator1&#39;: 83000001,</span></div><div class='line' id='LC170'><span class="c">#                       &#39;Simulator2&#39;: 83000002,</span></div><div class='line' id='LC171'><span class="c">#                       &#39;Simulator3&#39;: 83000003</span></div><div class='line' id='LC172'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">listeners</span> <span class="o">=</span> <span class="nb">set</span><span class="p">()</span>  </div><div class='line' id='LC173'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">prepareDevices</span><span class="p">()</span></div><div class='line' id='LC174'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC175'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">initContext</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC176'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Initialize a new context object.&quot;&quot;&quot;</span></div><div class='line' id='LC177'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">listeners</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">c</span><span class="o">.</span><span class="n">ID</span><span class="p">)</span></div><div class='line' id='LC178'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC179'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">expireContext</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC180'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">listeners</span><span class="o">.</span><span class="n">remove</span><span class="p">(</span><span class="n">c</span><span class="o">.</span><span class="n">ID</span><span class="p">)</span></div><div class='line' id='LC181'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC182'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getOtherListeners</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span><span class="n">c</span><span class="p">):</span></div><div class='line' id='LC183'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">notified</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">listeners</span><span class="o">.</span><span class="n">copy</span><span class="p">()</span></div><div class='line' id='LC184'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">notified</span><span class="o">.</span><span class="n">remove</span><span class="p">(</span><span class="n">c</span><span class="o">.</span><span class="n">ID</span><span class="p">)</span></div><div class='line' id='LC185'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">notified</span></div><div class='line' id='LC186'><br/></div><div class='line' id='LC187'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">prepareDevices</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></div><div class='line' id='LC188'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span> <span class="o">=</span> <span class="n">APTMotor</span><span class="p">()</span>        </div><div class='line' id='LC189'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">numberOfHardwareUnits</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getNumberOfHardwareUnits</span><span class="p">()</span></div><div class='line' id='LC190'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">connectedSerials</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getSerialNumber</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">numberOfHardwareUnits</span><span class="p">)]</span></div><div class='line' id='LC191'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">print</span> <span class="s">&#39;{} units connected: {}&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">numberOfHardwareUnits</span><span class="p">,</span><span class="n">connectedSerials</span><span class="p">)</span></div><div class='line' id='LC192'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">stage</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">deviceDict</span><span class="o">.</span><span class="n">values</span><span class="p">():</span></div><div class='line' id='LC193'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">stage</span><span class="o">.</span><span class="n">serial</span> <span class="ow">in</span> <span class="n">connectedSerials</span><span class="p">:</span></div><div class='line' id='LC194'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ok</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">initializeHardwareDevice</span><span class="p">(</span><span class="n">stage</span><span class="o">.</span><span class="n">serial</span><span class="p">)</span></div><div class='line' id='LC195'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">ok</span><span class="p">:</span> <span class="n">stage</span><span class="o">.</span><span class="n">initialized</span> <span class="o">=</span> <span class="bp">True</span></div><div class='line' id='LC196'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">setStageAxisInformation</span><span class="p">(</span><span class="n">stage</span><span class="o">.</span><span class="n">serial</span><span class="p">,</span> <span class="n">stage</span><span class="o">.</span><span class="n">minpos</span><span class="p">,</span> <span class="n">stage</span><span class="o">.</span><span class="n">maxpos</span><span class="p">)</span></div><div class='line' id='LC197'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC198'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getInitialized</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></div><div class='line' id='LC199'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">initialized</span> <span class="o">=</span> <span class="p">[</span><span class="n">stage</span><span class="o">.</span><span class="n">name</span> <span class="k">for</span> <span class="n">stage</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">deviceDict</span><span class="o">.</span><span class="n">values</span><span class="p">()</span> <span class="k">if</span> <span class="n">stage</span><span class="o">.</span><span class="n">initialized</span><span class="p">]</span></div><div class='line' id='LC200'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">initialized</span> </div><div class='line' id='LC201'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC202'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="s">&quot;Get Available Devices&quot;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span> <span class="s">&#39;*s&#39;</span><span class="p">)</span></div><div class='line' id='LC203'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getAvailableDevices</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC204'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Returns a List of Initialized Devices&quot;&quot;&quot;</span></div><div class='line' id='LC205'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">getInitialized</span><span class="p">()</span></div><div class='line' id='LC206'><br/></div><div class='line' id='LC207'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="s">&quot;Select Device&quot;</span><span class="p">,</span> <span class="n">name</span> <span class="o">=</span> <span class="s">&#39;s&#39;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span> <span class="s">&#39;&#39;</span><span class="p">)</span></div><div class='line' id='LC208'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">selectDevice</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span></div><div class='line' id='LC209'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">name</span> <span class="ow">not</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">getInitialized</span><span class="p">():</span> <span class="k">raise</span> <span class="ne">Exception</span><span class="p">(</span><span class="s">&quot;No such Device&quot;</span><span class="p">)</span></div><div class='line' id='LC210'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">deviceDict</span><span class="p">[</span><span class="n">name</span><span class="p">]</span><span class="o">.</span><span class="n">serial</span></div><div class='line' id='LC211'><br/></div><div class='line' id='LC212'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span> <span class="s">&quot;Get Serial Number&quot;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span> <span class="s">&#39;w&#39;</span><span class="p">)</span></div><div class='line' id='LC213'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getSerialNumber</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC214'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC215'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC216'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">serial</span></div><div class='line' id='LC217'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC218'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">3</span><span class="p">,</span> <span class="s">&quot;Get Device Information&quot;</span><span class="p">,</span>  <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;*s&#39;</span><span class="p">)</span></div><div class='line' id='LC219'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getHardwareInformation</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC220'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Returns Hardware Information: Model, Software Version, Hardware Notes&quot;&quot;&quot;</span></div><div class='line' id='LC221'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC222'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC223'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">c</span><span class="p">[</span><span class="s">&#39;Hardware Information&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getHardwareInformation</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">])</span></div><div class='line' id='LC224'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Hardware Information&#39;</span><span class="p">])</span></div><div class='line' id='LC225'><br/></div><div class='line' id='LC226'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">4</span><span class="p">,</span> <span class="s">&quot;Get Velocity Parameters&quot;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;*v&#39;</span><span class="p">)</span></div><div class='line' id='LC227'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getVelocityParameters</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC228'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Returns Velocity Parameters: Minimum Velocity, Acceleration, Maximum Velocity&quot;&quot;&quot;</span></div><div class='line' id='LC229'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC230'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC231'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">c</span><span class="p">[</span><span class="s">&#39;Velocity Parameters&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getVelocityParameters</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">])</span></div><div class='line' id='LC232'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Velocity Parameters&#39;</span><span class="p">])</span></div><div class='line' id='LC233'><br/></div><div class='line' id='LC234'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">5</span><span class="p">,</span> <span class="s">&quot;Get Velocity Parameter Limits&quot;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;*v&#39;</span><span class="p">)</span></div><div class='line' id='LC235'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getVelocityParameterLimits</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC236'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Returns Velocity Parameter Limits: Maximum Acceleration, Maximum Velocity&quot;&quot;&quot;</span></div><div class='line' id='LC237'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC238'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC239'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">c</span><span class="p">[</span><span class="s">&#39;Velocity Parameter Limits&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getVelocityParameterLimits</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">])</span></div><div class='line' id='LC240'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Velocity Parameter Limits&#39;</span><span class="p">])</span></div><div class='line' id='LC241'><br/></div><div class='line' id='LC242'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">6</span><span class="p">,</span> <span class="s">&quot;Set Velocity Parameters&quot;</span><span class="p">,</span> <span class="n">minimumVelocity</span> <span class="o">=</span> <span class="s">&#39;v&#39;</span><span class="p">,</span> <span class="n">acceleration</span> <span class="o">=</span> <span class="s">&#39;v&#39;</span><span class="p">,</span> <span class="n">maximumVelocity</span> <span class="o">=</span> <span class="s">&#39;v&#39;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;b&#39;</span><span class="p">)</span></div><div class='line' id='LC243'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">setVelocityParameters</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">,</span> <span class="n">minimumVelocity</span><span class="p">,</span> <span class="n">acceleration</span><span class="p">,</span> <span class="n">maximumVelocity</span><span class="p">):</span></div><div class='line' id='LC244'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Sets Velocity Parameters</span></div><div class='line' id='LC245'><span class="sd">            Minimum Velocity, Acceleration, Maximum Velocity&quot;&quot;&quot;</span></div><div class='line' id='LC246'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC247'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC248'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ok</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">setVelocityParameters</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">],</span> <span class="n">minimumVelocity</span><span class="p">,</span> <span class="n">acceleration</span><span class="p">,</span> <span class="n">maximumVelocity</span><span class="p">)</span></div><div class='line' id='LC249'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">notified</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">getOtherListeners</span><span class="p">(</span><span class="n">c</span><span class="p">)</span></div><div class='line' id='LC250'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">onVelocityParameterChange</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">],</span> <span class="n">notified</span><span class="p">)</span></div><div class='line' id='LC251'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="bp">True</span><span class="p">)</span></div><div class='line' id='LC252'><br/></div><div class='line' id='LC253'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">7</span><span class="p">,</span> <span class="s">&quot;Get Position&quot;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;v&#39;</span><span class="p">)</span></div><div class='line' id='LC254'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getPosition</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC255'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Returns Current Position&quot;&quot;&quot;</span></div><div class='line' id='LC256'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC257'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC258'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">c</span><span class="p">[</span><span class="s">&#39;Current Position&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getPosition</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">])</span></div><div class='line' id='LC259'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Current Position&#39;</span><span class="p">])</span></div><div class='line' id='LC260'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC261'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">8</span><span class="p">,</span> <span class="s">&quot;Move Relative&quot;</span><span class="p">,</span> <span class="n">relativeDistance</span> <span class="o">=</span> <span class="s">&#39;v&#39;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;b&#39;</span><span class="p">)</span></div><div class='line' id='LC262'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">moveRelative</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">,</span> <span class="n">relativeDistance</span><span class="p">):</span></div><div class='line' id='LC263'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Moves the Motor by a Distance Relative to its Current Position&quot;&quot;&quot;</span></div><div class='line' id='LC264'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC265'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC266'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ok</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">moveRelative</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">],</span> <span class="n">relativeDistance</span><span class="p">)</span></div><div class='line' id='LC267'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">notified</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">getOtherListeners</span><span class="p">(</span><span class="n">c</span><span class="p">)</span></div><div class='line' id='LC268'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">onPositionChange</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">],</span> <span class="n">notified</span><span class="p">)</span></div><div class='line' id='LC269'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">ok</span><span class="p">)</span>    </div><div class='line' id='LC270'><br/></div><div class='line' id='LC271'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">9</span><span class="p">,</span> <span class="s">&quot;Move Absolute&quot;</span><span class="p">,</span> <span class="n">absolutePosition</span> <span class="o">=</span> <span class="s">&#39;v&#39;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;b&#39;</span><span class="p">)</span></div><div class='line' id='LC272'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">moveAbsolute</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">,</span> <span class="n">absolutePosition</span><span class="p">):</span></div><div class='line' id='LC273'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Moves the Motor an Absolute Position&quot;&quot;&quot;</span></div><div class='line' id='LC274'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC275'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC276'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ok</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">moveAbsolute</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">],</span> <span class="n">absolutePosition</span><span class="p">)</span></div><div class='line' id='LC277'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">notified</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">getOtherListeners</span><span class="p">(</span><span class="n">c</span><span class="p">)</span></div><div class='line' id='LC278'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">onPositionChange</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">],</span> <span class="n">notified</span><span class="p">)</span>   </div><div class='line' id='LC279'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">ok</span><span class="p">)</span>    </div><div class='line' id='LC280'><br/></div><div class='line' id='LC281'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span> <span class="s">&quot;Identify Device&quot;</span><span class="p">,</span> <span class="n">returns</span> <span class="o">=</span><span class="s">&#39;b&#39;</span><span class="p">)</span></div><div class='line' id='LC282'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">identifyDevice</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC283'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Identifies Device by Flashing Front Panel LED for a Few Seconds&quot;&quot;&quot;</span></div><div class='line' id='LC284'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC285'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC286'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ok</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">identify</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">])</span></div><div class='line' id='LC287'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">ok</span><span class="p">)</span></div><div class='line' id='LC288'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC289'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">@setting</span><span class="p">(</span><span class="mi">11</span><span class="p">,</span> <span class="s">&quot;Get Stage Axis Information&quot;</span><span class="p">,</span> <span class="n">returns</span><span class="o">=</span><span class="s">&#39;*v&#39;</span><span class="p">)</span></div><div class='line' id='LC290'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">getStageAxisInformation</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">c</span><span class="p">):</span></div><div class='line' id='LC291'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">serial</span> <span class="o">=</span> <span class="n">c</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&#39;Device&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC292'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="ow">not</span> <span class="n">serial</span><span class="p">:</span> <span class="k">raise</span> <span class="ne">Exception</span> <span class="p">(</span><span class="s">&quot;Device not selected&quot;</span><span class="p">)</span></div><div class='line' id='LC293'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">c</span><span class="p">[</span><span class="s">&#39;Stage Axis Information&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="k">yield</span> <span class="n">deferToThread</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">getStageAxisInformation</span><span class="p">,</span> <span class="n">c</span><span class="p">[</span><span class="s">&#39;Device&#39;</span><span class="p">])</span></div><div class='line' id='LC294'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">returnValue</span><span class="p">(</span><span class="n">c</span><span class="p">[</span><span class="s">&#39;Stage Axis Information&#39;</span><span class="p">])</span></div><div class='line' id='LC295'><br/></div><div class='line' id='LC296'><span class="c">#    @setting(12, &quot;Get Hardware Limit Switches&quot;, returns=&#39;*v&#39;)</span></div><div class='line' id='LC297'><span class="c">#    def getHardwareLimitSwitches(self, c):</span></div><div class='line' id='LC298'><span class="c">#        if (self.initializedDict[c[&#39;Device&#39;]] == True):</span></div><div class='line' id='LC299'><span class="c">#            c[&#39;Hardware Limit Switches&#39;] = yield deferToThread(self.aptMotor.getHardwareLimitSwitches, c[&#39;Device&#39;])</span></div><div class='line' id='LC300'><span class="c">#            returnValue(c[&#39;Hardware Limit Switches&#39;])</span></div><div class='line' id='LC301'><span class="c">##    Sample Output: [Value(2.0, None), Value(2.0, None)]</span></div><div class='line' id='LC302'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC303'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">stopServer</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>  </div><div class='line' id='LC304'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;Cleans up APT DLL before closing&quot;&quot;&quot;</span></div><div class='line' id='LC305'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">aptMotor</span><span class="o">.</span><span class="n">cleanUpAPT</span><span class="p">()</span></div><div class='line' id='LC306'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC307'><span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">&quot;__main__&quot;</span><span class="p">:</span></div><div class='line' id='LC308'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kn">from</span> <span class="nn">labrad</span> <span class="kn">import</span> <span class="n">util</span></div><div class='line' id='LC309'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">util</span><span class="o">.</span><span class="n">runServer</span><span class="p">(</span><span class="n">APTMotorServer</span><span class="p">())</span></div></pre></div>
          </td>
        </tr>
      </table>
  </div>

          </div>
        </div>
      </div>
    </div>

  </div>

<div class="frame frame-loading large-loading-area" style="display:none;" data-tree-list-url="/micramm/HaeffnerLabLattice/tree-list/0549a77bdb10ed62f3f0be14f802e7f8f184930a" data-blob-url-prefix="/micramm/HaeffnerLabLattice/blob/0549a77bdb10ed62f3f0be14f802e7f8f184930a">
  <img src="https://a248.e.akamai.net/assets.github.com/images/spinners/octocat-spinner-128.gif?1347543534" height="64" width="64">
</div>

        </div>
      </div>
      <div class="context-overlay"></div>
    </div>

      <div id="footer-push"></div><!-- hack for sticky footer -->
    </div><!-- end of wrapper - hack for sticky footer -->

      <!-- footer -->
      <div id="footer" >
        
  <div class="upper_footer">
     <div class="container clearfix">

       <!--[if IE]><h4 id="blacktocat_ie">GitHub Links</h4><![endif]-->
       <![if !IE]><h4 id="blacktocat">GitHub Links</h4><![endif]>

       <ul class="footer_nav">
         <h4>GitHub</h4>
         <li><a href="https://github.com/about">About</a></li>
         <li><a href="https://github.com/blog">Blog</a></li>
         <li><a href="https://github.com/features">Features</a></li>
         <li><a href="https://github.com/contact">Contact &amp; Support</a></li>
         <li><a href="https://github.com/training">Training</a></li>
         <li><a href="http://enterprise.github.com/">GitHub Enterprise</a></li>
         <li><a href="http://status.github.com/">Site Status</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Clients</h4>
         <li><a href="http://mac.github.com/">GitHub for Mac</a></li>
         <li><a href="http://windows.github.com/">GitHub for Windows</a></li>
         <li><a href="http://eclipse.github.com/">GitHub for Eclipse</a></li>
         <li><a href="http://mobile.github.com/">GitHub Mobile Apps</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Tools</h4>
         <li><a href="http://get.gaug.es/">Gauges: Web analytics</a></li>
         <li><a href="http://speakerdeck.com">Speaker Deck: Presentations</a></li>
         <li><a href="https://gist.github.com">Gist: Code snippets</a></li>

         <h4 class="second">Extras</h4>
         <li><a href="http://jobs.github.com/">Job Board</a></li>
         <li><a href="http://shop.github.com/">GitHub Shop</a></li>
         <li><a href="http://octodex.github.com/">The Octodex</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Documentation</h4>
         <li><a href="http://help.github.com/">GitHub Help</a></li>
         <li><a href="http://developer.github.com/">Developer API</a></li>
         <li><a href="http://github.github.com/github-flavored-markdown/">GitHub Flavored Markdown</a></li>
         <li><a href="http://pages.github.com/">GitHub Pages</a></li>
       </ul>

     </div><!-- /.site -->
  </div><!-- /.upper_footer -->

<div class="lower_footer">
  <div class="container clearfix">
    <!--[if IE]><div id="legal_ie"><![endif]-->
    <![if !IE]><div id="legal"><![endif]>
      <ul>
          <li><a href="https://github.com/site/terms">Terms of Service</a></li>
          <li><a href="https://github.com/site/privacy">Privacy</a></li>
          <li><a href="https://github.com/security">Security</a></li>
      </ul>

      <p>&copy; 2012 <span title="0.33810s from fe14.rs.github.com">GitHub</span> Inc. All rights reserved.</p>
    </div><!-- /#legal or /#legal_ie-->

  </div><!-- /.site -->
</div><!-- /.lower_footer -->

      </div><!-- /#footer -->

    

<div id="keyboard_shortcuts_pane" class="instapaper_ignore readability-extra" style="display:none">
  <h2>Keyboard Shortcuts <small><a href="#" class="js-see-all-keyboard-shortcuts">(see all)</a></small></h2>

  <div class="columns threecols">
    <div class="column first">
      <h3>Site wide shortcuts</h3>
      <dl class="keyboard-mappings">
        <dt>s</dt>
        <dd>Focus command bar</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>?</dt>
        <dd>Bring up this help dialog</dd>
      </dl>
    </div><!-- /.column.first -->

    <div class="column middle" style='display:none'>
      <h3>Commit list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selection down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selection up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>c <em>or</em> o <em>or</em> enter</dt>
        <dd>Open commit</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>y</dt>
        <dd>Expand URL to its canonical form</dd>
      </dl>
    </div><!-- /.column.first -->

    <div class="column last js-hidden-pane" style='display:none'>
      <h3>Pull request list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selection down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selection up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>o <em>or</em> enter</dt>
        <dd>Open issue</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt><span class="platform-mac">⌘</span><span class="platform-other">ctrl</span> <em>+</em> enter</dt>
        <dd>Submit comment</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt><span class="platform-mac">⌘</span><span class="platform-other">ctrl</span> <em>+</em> shift p</dt>
        <dd>Preview comment</dd>
      </dl>
    </div><!-- /.columns.last -->

  </div><!-- /.columns.equacols -->

  <div class="js-hidden-pane" style='display:none'>
    <div class="rule"></div>

    <h3>Issues</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>x</dt>
          <dd>Toggle selection</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open issue</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="platform-mac">⌘</span><span class="platform-other">ctrl</span> <em>+</em> enter</dt>
          <dd>Submit comment</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="platform-mac">⌘</span><span class="platform-other">ctrl</span> <em>+</em> shift p</dt>
          <dd>Preview comment</dd>
        </dl>
      </div><!-- /.column.first -->
      <div class="column last">
        <dl class="keyboard-mappings">
          <dt>c</dt>
          <dd>Create issue</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>l</dt>
          <dd>Create label</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>i</dt>
          <dd>Back to inbox</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>u</dt>
          <dd>Back to issues</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>/</dt>
          <dd>Focus issues search</dd>
        </dl>
      </div>
    </div>
  </div>

  <div class="js-hidden-pane" style='display:none'>
    <div class="rule"></div>

    <h3>Issues Dashboard</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open issue</dd>
        </dl>
      </div><!-- /.column.first -->
    </div>
  </div>

  <div class="js-hidden-pane" style='display:none'>
    <div class="rule"></div>

    <h3>Network Graph</h3>
    <div class="columns equacols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt><span class="badmono">←</span> <em>or</em> h</dt>
          <dd>Scroll left</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">→</span> <em>or</em> l</dt>
          <dd>Scroll right</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">↑</span> <em>or</em> k</dt>
          <dd>Scroll up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">↓</span> <em>or</em> j</dt>
          <dd>Scroll down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>t</dt>
          <dd>Toggle visibility of head labels</dd>
        </dl>
      </div><!-- /.column.first -->
      <div class="column last">
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">←</span> <em>or</em> shift h</dt>
          <dd>Scroll all the way left</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">→</span> <em>or</em> shift l</dt>
          <dd>Scroll all the way right</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">↑</span> <em>or</em> shift k</dt>
          <dd>Scroll all the way up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">↓</span> <em>or</em> shift j</dt>
          <dd>Scroll all the way down</dd>
        </dl>
      </div><!-- /.column.last -->
    </div>
  </div>

  <div class="js-hidden-pane" >
    <div class="rule"></div>
    <div class="columns threecols">
      <div class="column first js-hidden-pane" >
        <h3>Source Code Browsing</h3>
        <dl class="keyboard-mappings">
          <dt>t</dt>
          <dd>Activates the file finder</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>l</dt>
          <dd>Jump to line</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>w</dt>
          <dd>Switch branch/tag</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>y</dt>
          <dd>Expand URL to its canonical form</dd>
        </dl>
      </div>
    </div>
  </div>

  <div class="js-hidden-pane" style='display:none'>
    <div class="rule"></div>
    <div class="columns threecols">
      <div class="column first">
        <h3>Browsing Commits</h3>
        <dl class="keyboard-mappings">
          <dt><span class="platform-mac">⌘</span><span class="platform-other">ctrl</span> <em>+</em> enter</dt>
          <dd>Submit comment</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>escape</dt>
          <dd>Close form</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>p</dt>
          <dd>Parent commit</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o</dt>
          <dd>Other parent commit</dd>
        </dl>
      </div>
    </div>
  </div>

  <div class="js-hidden-pane" style='display:none'>
    <div class="rule"></div>
    <h3>Notifications</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open notification</dd>
        </dl>
      </div><!-- /.column.first -->

      <div class="column second">
        <dl class="keyboard-mappings">
          <dt>e <em>or</em> shift i <em>or</em> y</dt>
          <dd>Mark as read</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift m</dt>
          <dd>Mute thread</dd>
        </dl>
      </div><!-- /.column.first -->
    </div>
  </div>

</div>

    <div id="markdown-help" class="instapaper_ignore readability-extra">
  <h2>Markdown Cheat Sheet</h2>

  <div class="cheatsheet-content">

  <div class="mod">
    <div class="col">
      <h3>Format Text</h3>
      <p>Headers</p>
      <pre>
# This is an &lt;h1&gt; tag
## This is an &lt;h2&gt; tag
###### This is an &lt;h6&gt; tag</pre>
     <p>Text styles</p>
     <pre>
*This text will be italic*
_This will also be italic_
**This text will be bold**
__This will also be bold__

*You **can** combine them*
</pre>
    </div>
    <div class="col">
      <h3>Lists</h3>
      <p>Unordered</p>
      <pre>
* Item 1
* Item 2
  * Item 2a
  * Item 2b</pre>
     <p>Ordered</p>
     <pre>
1. Item 1
2. Item 2
3. Item 3
   * Item 3a
   * Item 3b</pre>
    </div>
    <div class="col">
      <h3>Miscellaneous</h3>
      <p>Images</p>
      <pre>
![GitHub Logo](/images/logo.png)
Format: ![Alt Text](url)
</pre>
     <p>Links</p>
     <pre>
http://github.com - automatic!
[GitHub](http://github.com)</pre>
<p>Blockquotes</p>
     <pre>
As Kanye West said:

> We're living the future so
> the present is our past.
</pre>
    </div>
  </div>
  <div class="rule"></div>

  <h3>Code Examples in Markdown</h3>
  <div class="col">
      <p>Syntax highlighting with <a href="http://github.github.com/github-flavored-markdown/" title="GitHub Flavored Markdown" target="_blank">GFM</a></p>
      <pre>
```javascript
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }
}
```</pre>
    </div>
    <div class="col">
      <p>Or, indent your code 4 spaces</p>
      <pre>
Here is a Python code example
without syntax highlighting:

    def foo:
      if not bar:
        return true</pre>
    </div>
    <div class="col">
      <p>Inline code for comments</p>
      <pre>
I think you should use an
`&lt;addr&gt;` element here instead.</pre>
    </div>
  </div>

  </div>
</div>


    <div id="ajax-error-message" class="flash flash-error">
      <span class="mini-icon mini-icon-exclamation"></span>
      Something went wrong with that request. Please try again.
      <a href="#" class="mini-icon mini-icon-remove-close ajax-error-dismiss"></a>
    </div>

    <div id="logo-popup">
      <h2>Looking for the GitHub logo?</h2>
      <ul>
        <li>
          <h4>GitHub Logo</h4>
          <a href="http://github-media-downloads.s3.amazonaws.com/GitHub_Logos.zip"><img alt="Github_logo" src="https://a248.e.akamai.net/assets.github.com/images/modules/about_page/github_logo.png?1329921026" /></a>
          <a href="http://github-media-downloads.s3.amazonaws.com/GitHub_Logos.zip" class="minibutton download">Download</a>
        </li>
        <li>
          <h4>The Octocat</h4>
          <a href="http://github-media-downloads.s3.amazonaws.com/Octocats.zip"><img alt="Octocat" src="https://a248.e.akamai.net/assets.github.com/images/modules/about_page/octocat.png?1329921026" /></a>
          <a href="http://github-media-downloads.s3.amazonaws.com/Octocats.zip" class="minibutton download">Download</a>
        </li>
      </ul>
    </div>

    
    
    <span id='server_response_time' data-time='0.34361' data-host='fe14'></span>
    
  </body>
</html>

