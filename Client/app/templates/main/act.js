/**
 * Created by panda on 6/7/18.
 */

username = request.querystring("username");
password = request.querystring("password");
response.write(username);
response.write(password);