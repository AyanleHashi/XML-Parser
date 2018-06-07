# XML-Parser
A WIP script for extracting publication data from the Cancer Imaging Archive publication list (last updated May 2018). Requires the `bs4` module and the lxml tree builder, you can install them by doing `pip install bs4` and `pip install lxml`.

Example output:

<html>
<h3>Robust Computer-Aided Detection of Pulmonary Nodules from Chest Computed Tomography</h3>
  Abduh, Zaid; Wahed, Manal Abdel; Kadah, Yasser M
  <br>
  <periodical>Journal of Medical Imaging and Health Informatics</periodical>, 2016
  <pub-type> - Journal Article</pub-type>
</html>


Alternatively:
<html>
  <table style="width:100%">
    <tr>
      <th>Authors</th>
      <th>Title</th>
      <th>Periodical</th>
      <th>Year</th>
      <th>Publication Type</th>
    </tr>
    <tr>
        <td>Abduh, Zaid; Wahed, Manal Abdel; Kadah, Yasser M</td>
        <td>Robust Computer-Aided Detection of Pulmonary Nodules from Chest Computed Tomography</td>
        <td>Journal of Medical Imaging and Health Informatics</td>
        <td>2016</td>
        <td>Journal Article</td>
    </tr>

  </table>
</html>
