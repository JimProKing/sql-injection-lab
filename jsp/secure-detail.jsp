<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%
    String DB_HOST = "jdbc:mysql://127.0.0.1:3306/sqli_lab?useSSL=false&serverTimezone=UTC";
    String DB_USER = "root";
    String DB_PASSWORD = "ntsdev";

    String id = request.getParameter("id");
    String message = "";
    String userInfo = "";

    if (id != null && !id.trim().isEmpty()) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(DB_HOST, DB_USER, DB_PASSWORD);

            // SECURE
            String sql = "SELECT id, username, email, role FROM users WHERE id = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, Integer.parseInt(id));   // also safe to use setString

            rs = pstmt.executeQuery();

            if (rs.next()) {
                userInfo = "ID: " + rs.getInt("id") + "<br>" +
                           "Username: " + rs.getString("username") + "<br>" +
                           "Email: " + rs.getString("email") + "<br>" +
                           "Role: " + rs.getString("role");
            } else {
                userInfo = "사용자 없음";
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
<head><meta charset="UTF-8"><title>Secure Detail</title>
<style>body { font-family: monospace; max-width: 800px; margin: 40px auto; }</style>
</head>
<body>
    <h1>Secure User Detail (PreparedStatement)</h1>

    <form method="get">
        ID: <input type="text" name="id" value="<%= id != null ? id : "1" %>">
        <input type="submit" value="조회">
    </form>

    <p><%= userInfo %></p>
    <% if (!message.isEmpty()) { %><p style="color:red"><%= message %></p><% } %>

    <p><strong>핵심:</strong> <code>?</code> 플레이스홀더를 사용하면 id 파라미터에 <code>1 AND 1=1</code> 같은 값을 넣어도 구조가 깨지지 않습니다.</p>

    <p><a href="vuln-detail.jsp">Vulnerable 버전 보기</a></p>
</body>
</html>