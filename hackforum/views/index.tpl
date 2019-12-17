% include('skele_header.tpl')


  <div class="container">
  
  <h1> Hello there {{user["username"] }} </h1>
  
  <table class="table">
  <thead><tr><th>Username</th><th>Comments</th></tr></thead>
  %for comm in comments:
  <tr>  
    <td>{{ comm["username"] }}</td>
    <td>{{! comm["comment"] }}</td>
  </tr>  
  %end
  </table>
  <br>
  <h3> Enter comment: </h3>
  <form action="/" method="post">
    <input class="smooth" type="text" placeholder="Enter comment" name="comment" size="64" style="width:auto;" required>
    <button class="btn btn-sm btn-b" type="submit">Send comment</button>
  </form>
  </div>
  
  
% include('skele_footer.tpl')

