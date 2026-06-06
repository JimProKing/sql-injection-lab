<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%--
    SQL Injection Lab - VULNERABLE LOGIN (JSP + JDBC)

    This file intentionally uses Statement + string concatenation.
    Compare with secure-login.jsp

    Prerequisites:
    - MySQL running
    - Database "sqli_lab" created (see ../db_setup_mysql.sql)
    - MySQL JDBC driver in Tomcat's lib/ or WEB-INF/lib/
--%>
<%
    String DB_HOST = "jdbc:mysql://127.0.0.1:3306/sqli_lab?useSSL=false&serverTimezone=UTC";
    String DB_USER = "root";
    String DB_PASSWORD = "ntsdev";

    String username = request.getParameter("username");
    String password = request.getParameter("password");

    String message = "";
    String executedQuery = "";
    boolean loggedIn = false;
    String userRole = "";
    String secret = "";

    if (username != null && password != null) {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(DB_HOST, DB_USER, DB_PASSWORD);
            stmt = conn.createStatement();

            // VULNERABLE: Direct string concatenation
            executedQuery = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";

            rs = stmt.executeQuery(executedQuery);

            if (rs.next()) {
                loggedIn = true;
                userRole = rs.getString("role");
                secret = rs.getString("secret_note");
                message = "<span style='color:green;font-weight:bold'>로그인 성공!</span> " +
                          "환영합니다, <strong>" + rs.getString("username") + "</strong> (role: " + userRole + ")";
            } else {
                message = "<span style='color:red'>로그인 실패</span> - 아이디 또는 비밀번호가 올바르지 않습니다.";
            }
        } catch (Exception e) {
            message = "<span style='color:red'>에러: " + e.getMessage() + "</span>";
        } finally {
            try { if (rs != null) rs.close(); } catch (Exception ignored) {}
            try { if (stmt != null) stmt.close(); } catch (Exception ignored) {}
            try { if (conn != null) conn.close(); } catch (Exception ignored) {}
        }
    }
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SQLi Lab - Vulnerable Login (JSP)</title>
    <style>
        body { font-family: monospace; max-width: 860px; margin: 40px auto; }
        pre { background: #1a1a1a; color: #0f0; padding: 14px; overflow-x: auto; }
        .box { background: #f8f8f8; padding: 20px; border: 1px solid #ccc; margin: 15px 0; }
        input { font-family: monospace; font-size: 15px; padding: 6px; }
    </style>
</head>
<body>
    <h1>SQL Injection Lab - Vulnerable Login (JSP)</h1>
    <p style="color:#c00"><strong>의도적으로 취약하게 만든 예제입니다.</strong></p>

    <div class="box">
        <form method="post">
            <p>Username: <input type="text" name="username" size="30" value="<%= username != null ? username : "" %>"></p>
            <p>Password: <input type="text" name="password" size="30" value="<%= password != null ? password : "" %>"></p>
            <p><input type="submit" value="로그인"></p>
        </form>
    </div>

    <% if (!executedQuery.isEmpty()) { %>
        <h3>실제로 실행된 쿼리 (공격자에게 노출되는 정보):</h3>
        <pre><%= executedQuery %></pre>
    <% } %>

    <% if (!message.isEmpty()) { %>
        <div class="box">
            <p><%= message %></p>
            <% if (loggedIn) { %>
                <p><strong>Secret Note:</strong> <%= secret %></p>
            <% } %>
        </div>
    <% } %>

    <h3>공격 페이로드 예시</h3>
    <ul>
        <li><code>admin' -- </code></li>
        <li><code>admin' OR '1'='1' -- </code></li>
        <li><code>' OR 1=1#</code></li>
        <li><code>admin' OR '1'='1' /* 주석 */</code></li>
        <li><code>crehacktive' AND password LIKE 'P@%' -- </code></li>
    </ul>

    <p>
        <a href="vuln-search.jsp">다음 예제: UNION 검색 →</a><br>
        <a href="secure-login.jsp">비교: Secure 버전 보기</a><br>
        <a href="/">홈 (상위 폴더)</a>
    </p>
</body>
</html>