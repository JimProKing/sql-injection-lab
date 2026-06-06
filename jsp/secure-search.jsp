<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%--
    SECURE version of the search page using PreparedStatement.
--%>
<%
    String DB_HOST = "jdbc:mysql://127.0.0.1:3306/sqli_lab?useSSL=false&serverTimezone=UTC";
    String DB_USER = "root";
    String DB_PASSWORD = "ntsdev";

    String keyword = request.getParameter("q");
    String message = "";
    java.util.List<String[]> results = new java.util.ArrayList<>();

    if (keyword != null && !keyword.trim().isEmpty()) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(DB_HOST, DB_USER, DB_PASSWORD);

            // SECURE
            String sql = "SELECT id, name, price, description FROM products " +
                         "WHERE name LIKE ? OR description LIKE ?";
            pstmt = conn.prepareStatement(sql);
            String like = "%" + keyword + "%";
            pstmt.setString(1, like);
            pstmt.setString(2, like);

            rs = pstmt.executeQuery();

            while (rs.next()) {
                results.add(new String[]{
                    rs.getString("id"),
                    rs.getString("name"),
                    rs.getString("price"),
                    rs.getString("description")
                });
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
<head>
    <meta charset="UTF-8">
    <title>Secure Search - SQLi Lab</title>
    <style>body { font-family: monospace; max-width: 960px; margin: 40px auto; } .box{background:#f8f8f8;padding:15px;border:1px solid #ccc}</style>
</head>
<body>
    <h1>Secure Search (PreparedStatement)</h1>
    <p style="color:#090">이 버전은 UNION 인젝션이 동작하지 않습니다.</p>

    <div class="box">
        <form method="get">
            검색어: <input type="text" name="q" size="50" value="<%= keyword != null ? keyword : "" %>">
            <input type="submit" value="검색">
        </form>
    </div>

    <% if (!results.isEmpty()) { %>
        <h3>검색 결과</h3>
        <table border="1" cellpadding="8">
            <tr><th>ID</th><th>Name</th><th>Price</th><th>Description</th></tr>
            <% for (String[] r : results) { %>
                <tr><td><%= r[0] %></td><td><%= r[1] %></td><td><%= r[2] %></td><td><%= r[3] %></td></tr>
            <% } %>
        </table>
    <% } else if (keyword != null) { %>
        <p>결과 없음</p>
    <% } %>

    <p><a href="vuln-search.jsp">Vulnerable 버전 보기</a></p>
</body>
</html>