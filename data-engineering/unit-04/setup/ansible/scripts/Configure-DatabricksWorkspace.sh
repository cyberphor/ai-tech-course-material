if test -f ~/.databrickscfg; then
  rm ~/.databrickscfg
fi
echo "[DEFAULT]" > ~/.databrickscfg
echo "host = ${DATABRICKS_HOST}" >> ~/.databrickscfg
echo "token = ${DATABRICKS_TOKEN}" >> ~/.databrickscfg