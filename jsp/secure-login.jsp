<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%--
    SECURE version using PreparedStatement + parameterized query.
    This is the correct pattern.
--%>
<%
    String DB_HOST = "jdbc:mysql://127.0.0.1:3306/sqli_lab?useSSL=false&serverTimezone=UTC";
    String DB_USER = "root";
    String DB_PASSWORD = "ntsdev";

    String username = request.getParameter("username");
    String password = request.getParameter("password");

    String message = "";
    String userRole = "";

    if (username != null && password != null) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(DB_HOST, DB_USER, DB_PASSWORD);

            // SECURE: PreparedStatement with placeholders
            String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, username);
            pstmt.setString(2, password);

            rs = pstmt.executeQuery();

            if (rs.next()) {
                userRole = rs.getString("role");
                message = "<span style='color:green'>로그인 성공 (SECURE)</span> " +
                          "환영합니다, <strong>" + rs.getString("username") + "</strong>";
            } else {
                message = "<span style='color:red'>로그인 실패</span>";
            }
        } catch (Exception e) {
            message = "Error: " + e.getMessage();
        } finally {
            try { if (rs != null) rs.close(); } catch (Exception ignored) {}
            try { if (pstmt != null) pstmt.close(); } catch (Exception ignored) {}
            try { if (conn != null) conn.close(); } catch (Exception ignored) {}
        }
    }
%>
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Secure Login</title>
<style>body { font-family: monospace; max-width: 800px; margin: 40px auto; } pre { background:#f0f0f0; padding:12px; }</style>
</head>
<body>
    <h1>Secure Login (PreparedStatement)</h1>
    <p style="color:#090">이 버전은 SQL 인젝션 공격이 동작하지 않습니다.</p>

    <form method="post">
        <p>Username: <input type="text" name="username" size="30"></p>
        <p>Password: <input type="text" name="password" size="30"></p>
        <p><input type="submit" value="로그인"></p>
    </form>

    <p><%= message %></p>

    <h3>핵심 차이점 (Secure)</h3>
    <pre>
String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, username);
pstmt.setString(2, password);
ResultSet rs = pstmt.executeQuery();
    </pre>

    <p>입력값에 들어간 <code>' OR 1=1 --</code> 같은 문자열은 <strong>데이터 값</strong>으로만 취급됩니다.</p>

    <p><a href="vuln-login.jsp">Vulnerable 버전으로 돌아가기</a></p>
</body>
</html>