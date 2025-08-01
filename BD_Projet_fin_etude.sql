PGDMP  ,                     }            Evaluation_enseignants    17.4    17.4 )    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16387    Evaluation_enseignants    DATABASE     �   CREATE DATABASE "Evaluation_enseignants" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
 (   DROP DATABASE "Evaluation_enseignants";
                     postgres    false            �            1255    33067 s   creer_administrateur(character varying, character varying, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION public.creer_administrateur(p_ut_id character varying, p_ut_np character varying, p_ut_sx character varying, p_ut_ac character varying, p_ut_fo character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO utilisateur (
        ut_id, ut_np, ut_sx, ut_ac,
        ut_st, ut_sp, ut_gr, ut_fi, ut_ma, ut_fo
    ) VALUES (
        p_ut_id, p_ut_np, p_ut_sx, p_ut_ac,
        'A', NULL, NULL, NULL, p_ut_id, p_ut_fo
    );
END;
$$;
 �   DROP FUNCTION public.creer_administrateur(p_ut_id character varying, p_ut_np character varying, p_ut_sx character varying, p_ut_ac character varying, p_ut_fo character varying);
       public               postgres    false            �            1255    33043 G   sp_creer_cours(character varying, character varying, character varying) 	   PROCEDURE     �  CREATE PROCEDURE public.sp_creer_cours(IN p_co_co character varying, IN p_co_ti character varying, IN p_co_ty character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si le cours existe déjà
    IF EXISTS (SELECT 1 FROM Cours WHERE CO_CO = p_co_co) THEN
        p_resultat := 'ERREUR: Cours avec ce code existe déjà';
        RETURN;
    END IF;
    
    -- Insérer le nouveau cours
    INSERT INTO Cours (CO_CO, CO_TI, CO_TY)
    VALUES (p_co_co, p_co_ti, p_co_ty);
    
    p_resultat := 'SUCCÈS: Cours créé avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 �   DROP PROCEDURE public.sp_creer_cours(IN p_co_co character varying, IN p_co_ti character varying, IN p_co_ty character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33047 j   sp_creer_enseignement(character varying, numeric, character varying, character varying, character varying) 	   PROCEDURE     .  CREATE PROCEDURE public.sp_creer_enseignement(IN p_en_co character varying, IN p_en_ac numeric, IN p_en_sm character varying, IN p_en_cc character varying, IN p_en_cr character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'enseignement existe déjà
    IF EXISTS (SELECT 1 FROM Enseignement WHERE EN_CO = p_en_co) THEN
        p_resultat := 'ERREUR: Enseignement avec ce code existe déjà';
        RETURN;
    END IF;
    
    -- Insérer le nouvel enseignement
    INSERT INTO Enseignement (EN_CO, EN_AC, EN_SM, EN_CC, EN_CR)
    VALUES (p_en_co, p_en_ac, p_en_sm, p_en_cc, p_en_cr);
    
    p_resultat := 'SUCCÈS: Enseignement créé avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 �   DROP PROCEDURE public.sp_creer_enseignement(IN p_en_co character varying, IN p_en_ac numeric, IN p_en_sm character varying, IN p_en_cc character varying, IN p_en_cr character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33051 I  sp_creer_evaluation(character varying, date, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying) 	   PROCEDURE     �  CREATE PROCEDURE public.sp_creer_evaluation(IN p_ev_id character varying, IN p_ev_da date, IN p_ev_clex character varying, IN p_ev_pen character varying, IN p_ev_ped character varying, IN p_ev_acco character varying, IN p_ev_inco character varying, IN p_ev_atte character varying, IN p_ev_getco character varying, IN p_ev_encpa character varying, IN p_ev_usoup character varying, IN p_ev_intre character varying, IN p_ev_intco character varying, IN p_ev_clobp character varying, IN p_ev_utcoc character varying, IN p_ev_oble character varying, IN p_ev_coeve character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'évaluation existe déjà
    IF EXISTS (SELECT 1 FROM Evaluation WHERE EV_ID = p_ev_id) THEN
        p_resultat := 'ERREUR: Évaluation avec cet ID existe déjà';
        RETURN;
    END IF;
    
    -- Insérer la nouvelle évaluation
    INSERT INTO Evaluation (
        EV_ID, EV_DA, EV_CLEX, EV_PEN, EV_PED, EV_ACCO, EV_INCO, EV_ATTE, 
        EV_GETCO, EV_ENCPA, EV_USOUP, EV_INTRE, EV_INTCO, EV_CLOBP, 
        EV_UTCOC, EV_OBLE, EV_COEVE
    )
    VALUES (
        p_ev_id, p_ev_da, p_ev_clex, p_ev_pen, p_ev_ped, p_ev_acco, p_ev_inco, 
        p_ev_atte, p_ev_getco, p_ev_encpa, p_ev_usoup, p_ev_intre, p_ev_intco, 
        p_ev_clobp, p_ev_utcoc, p_ev_oble, p_ev_coeve
    );
    
    p_resultat := 'SUCCÈS: Évaluation créée avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 U  DROP PROCEDURE public.sp_creer_evaluation(IN p_ev_id character varying, IN p_ev_da date, IN p_ev_clex character varying, IN p_ev_pen character varying, IN p_ev_ped character varying, IN p_ev_acco character varying, IN p_ev_inco character varying, IN p_ev_atte character varying, IN p_ev_getco character varying, IN p_ev_encpa character varying, IN p_ev_usoup character varying, IN p_ev_intre character varying, IN p_ev_intco character varying, IN p_ev_clobp character varying, IN p_ev_utcoc character varying, IN p_ev_oble character varying, IN p_ev_coeve character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33039 �   sp_creer_utilisateur(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying) 	   PROCEDURE       CREATE PROCEDURE public.sp_creer_utilisateur(IN p_ut_id character varying, IN p_ut_np character varying, IN p_ut_sx character varying, IN p_ut_ac character varying, IN p_ut_st character varying, IN p_ut_sp character varying, IN p_ut_gr character varying, IN p_ut_fi character varying, IN p_ut_ma character varying, IN p_ut_fo character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'utilisateur existe déjà
    IF EXISTS (SELECT 1 FROM Utilisateur WHERE UT_ID = p_ut_id) THEN
        p_resultat := 'ERREUR: Utilisateur avec cet ID existe déjà';
        RETURN;
    END IF;
    
    -- Insérer le nouvel utilisateur
    INSERT INTO Utilisateur (UT_ID, UT_NP, UT_SX, UT_AC, UT_ST, UT_SP, UT_GR, UT_FI, UT_MA, UT_FO)
    VALUES (p_ut_id, p_ut_np, p_ut_sx, p_ut_ac, p_ut_st, p_ut_sp, p_ut_gr, p_ut_fi, p_ut_ma, p_ut_fo);
    
    p_resultat := 'SUCCÈS: Utilisateur créé avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 m  DROP PROCEDURE public.sp_creer_utilisateur(IN p_ut_id character varying, IN p_ut_np character varying, IN p_ut_sx character varying, IN p_ut_ac character varying, IN p_ut_st character varying, IN p_ut_sp character varying, IN p_ut_gr character varying, IN p_ut_fi character varying, IN p_ut_ma character varying, IN p_ut_fo character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33046 +   sp_lister_cours_par_type(character varying)    FUNCTION     }  CREATE FUNCTION public.sp_lister_cours_par_type(p_type character varying DEFAULT NULL::character varying) RETURNS TABLE(co_co character varying, co_ti character varying, co_ty character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT c.CO_CO, c.CO_TI, c.CO_TY
    FROM Cours c
    WHERE (p_type IS NULL OR c.CO_TY = p_type)
    ORDER BY c.CO_TI;
END;
$$;
 I   DROP FUNCTION public.sp_lister_cours_par_type(p_type character varying);
       public               postgres    false            �            1255    33050 *   sp_lister_enseignements_par_annee(numeric)    FUNCTION     �  CREATE FUNCTION public.sp_lister_enseignements_par_annee(p_annee numeric) RETURNS TABLE(en_co character varying, en_ac numeric, en_sm character varying, en_cc character varying, en_cr character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT e.EN_CO, e.EN_AC, e.EN_SM, e.EN_CC, e.EN_CR
    FROM Enseignement e
    WHERE e.EN_AC = p_annee
    ORDER BY e.EN_SM, e.EN_CR;
END;
$$;
 I   DROP FUNCTION public.sp_lister_enseignements_par_annee(p_annee numeric);
       public               postgres    false            �            1255    33054 -   sp_lister_evaluations_par_periode(date, date)    FUNCTION     �  CREATE FUNCTION public.sp_lister_evaluations_par_periode(p_date_debut date, p_date_fin date) RETURNS TABLE(ev_id character varying, ev_da date, ev_clex character varying, ev_pen character varying, ev_ped character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT e.EV_ID, e.EV_DA, e.EV_CLEX, e.EV_PEN, e.EV_PED
    FROM Evaluation e
    WHERE e.EV_DA BETWEEN p_date_debut AND p_date_fin
    ORDER BY e.EV_DA DESC;
END;
$$;
 \   DROP FUNCTION public.sp_lister_evaluations_par_periode(p_date_debut date, p_date_fin date);
       public               postgres    false            �            1255    33044 J   sp_modifier_cours(character varying, character varying, character varying) 	   PROCEDURE     �  CREATE PROCEDURE public.sp_modifier_cours(IN p_co_co character varying, IN p_co_ti character varying, IN p_co_ty character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si le cours existe
    IF NOT EXISTS (SELECT 1 FROM Cours WHERE CO_CO = p_co_co) THEN
        p_resultat := 'ERREUR: Cours introuvable';
        RETURN;
    END IF;
    
    -- Mettre à jour le cours
    UPDATE Cours 
    SET CO_TI = p_co_ti,
        CO_TY = p_co_ty
    WHERE CO_CO = p_co_co;
    
    p_resultat := 'SUCCÈS: Cours modifié avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 �   DROP PROCEDURE public.sp_modifier_cours(IN p_co_co character varying, IN p_co_ti character varying, IN p_co_ty character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33048 m   sp_modifier_enseignement(character varying, numeric, character varying, character varying, character varying) 	   PROCEDURE     ;  CREATE PROCEDURE public.sp_modifier_enseignement(IN p_en_co character varying, IN p_en_ac numeric, IN p_en_sm character varying, IN p_en_cc character varying, IN p_en_cr character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'enseignement existe
    IF NOT EXISTS (SELECT 1 FROM Enseignement WHERE EN_CO = p_en_co) THEN
        p_resultat := 'ERREUR: Enseignement introuvable';
        RETURN;
    END IF;
    
    -- Mettre à jour l'enseignement
    UPDATE Enseignement 
    SET EN_AC = p_en_ac,
        EN_SM = p_en_sm,
        EN_CC = p_en_cc,
        EN_CR = p_en_cr
    WHERE EN_CO = p_en_co;
    
    p_resultat := 'SUCCÈS: Enseignement modifié avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 �   DROP PROCEDURE public.sp_modifier_enseignement(IN p_en_co character varying, IN p_en_ac numeric, IN p_en_sm character varying, IN p_en_cc character varying, IN p_en_cr character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33052 L  sp_modifier_evaluation(character varying, date, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying) 	   PROCEDURE     /  CREATE PROCEDURE public.sp_modifier_evaluation(IN p_ev_id character varying, IN p_ev_da date, IN p_ev_clex character varying, IN p_ev_pen character varying, IN p_ev_ped character varying, IN p_ev_acco character varying, IN p_ev_inco character varying, IN p_ev_atte character varying, IN p_ev_getco character varying, IN p_ev_encpa character varying, IN p_ev_usoup character varying, IN p_ev_intre character varying, IN p_ev_intco character varying, IN p_ev_clobp character varying, IN p_ev_utcoc character varying, IN p_ev_oble character varying, IN p_ev_coeve character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'évaluation existe
    IF NOT EXISTS (SELECT 1 FROM Evaluation WHERE EV_ID = p_ev_id) THEN
        p_resultat := 'ERREUR: Évaluation introuvable';
        RETURN;
    END IF;
    
    -- Mettre à jour l'évaluation
    UPDATE Evaluation 
    SET EV_DA = p_ev_da,
        EV_CLEX = p_ev_clex,
        EV_PEN = p_ev_pen,
        EV_PED = p_ev_ped,
        EV_ACCO = p_ev_acco,
        EV_INCO = p_ev_inco,
        EV_ATTE = p_ev_atte,
        EV_GETCO = p_ev_getco,
        EV_ENCPA = p_ev_encpa,
        EV_USOUP = p_ev_usoup,
        EV_INTRE = p_ev_intre,
        EV_INTCO = p_ev_intco,
        EV_CLOBP = p_ev_clobp,
        EV_UTCOC = p_ev_utcoc,
        EV_OBLE = p_ev_oble,
        EV_COEVE = p_ev_coeve
    WHERE EV_ID = p_ev_id;
    
    p_resultat := 'SUCCÈS: Évaluation modifiée avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 X  DROP PROCEDURE public.sp_modifier_evaluation(IN p_ev_id character varying, IN p_ev_da date, IN p_ev_clex character varying, IN p_ev_pen character varying, IN p_ev_ped character varying, IN p_ev_acco character varying, IN p_ev_inco character varying, IN p_ev_atte character varying, IN p_ev_getco character varying, IN p_ev_encpa character varying, IN p_ev_usoup character varying, IN p_ev_intre character varying, IN p_ev_intco character varying, IN p_ev_clobp character varying, IN p_ev_utcoc character varying, IN p_ev_oble character varying, IN p_ev_coeve character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33040 �   sp_modifier_utilisateur(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying) 	   PROCEDURE     Q  CREATE PROCEDURE public.sp_modifier_utilisateur(IN p_ut_id character varying, IN p_ut_np character varying, IN p_ut_sx character varying, IN p_ut_ac character varying, IN p_ut_st character varying, IN p_ut_sp character varying, IN p_ut_gr character varying, IN p_ut_fi character varying, IN p_ut_ma character varying, IN p_ut_fo character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'utilisateur existe
    IF NOT EXISTS (SELECT 1 FROM Utilisateur WHERE UT_ID = p_ut_id) THEN
        p_resultat := 'ERREUR: Utilisateur introuvable';
        RETURN;
    END IF;
    
    -- Mettre à jour l'utilisateur
    UPDATE Utilisateur 
    SET UT_NP = p_ut_np,
        UT_SX = p_ut_sx,
        UT_AC = p_ut_ac,
        UT_ST = p_ut_st,
        UT_SP = p_ut_sp,
        UT_GR = p_ut_gr,
        UT_FI = p_ut_fi,
        UT_MA = p_ut_ma,
        UT_FO = p_ut_fo
    WHERE UT_ID = p_ut_id;
    
    p_resultat := 'SUCCÈS: Utilisateur modifié avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 p  DROP PROCEDURE public.sp_modifier_utilisateur(IN p_ut_id character varying, IN p_ut_np character varying, IN p_ut_sx character varying, IN p_ut_ac character varying, IN p_ut_st character varying, IN p_ut_sp character varying, IN p_ut_gr character varying, IN p_ut_fi character varying, IN p_ut_ma character varying, IN p_ut_fo character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33057 !   sp_moyenne_evaluations_criteres()    FUNCTION     �  CREATE FUNCTION public.sp_moyenne_evaluations_criteres() RETURNS TABLE(critere character varying, moyenne_score numeric, nombre_evaluations bigint)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Cette fonction nécessite une conversion des valeurs textuelles en scores numériques
    -- Vous devrez adapter selon votre système de notation
    RETURN QUERY
    WITH scores AS (
        SELECT 
            'Pédagogie' as critere,
            CASE 
                WHEN EV_PED = 'Excellent' THEN 5
                WHEN EV_PED = 'Très Bien' THEN 4
                WHEN EV_PED = 'Bien' THEN 3
                WHEN EV_PED = 'Passable' THEN 2
                ELSE 1
            END as score
        FROM Evaluation
        WHERE EV_PED IS NOT NULL
    )
    SELECT 
        s.critere,
        AVG(s.score::NUMERIC)::NUMERIC(5,2) as moyenne_score,
        COUNT(*)::BIGINT as nombre_evaluations
    FROM scores s
    GROUP BY s.critere;
END;
$$;
 8   DROP FUNCTION public.sp_moyenne_evaluations_criteres();
       public               postgres    false                       1255    33061 &   sp_nettoyer_donnees_obsoletes(integer)    FUNCTION     o  CREATE FUNCTION public.sp_nettoyer_donnees_obsoletes(p_annees_retention integer DEFAULT 5) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
    date_limite DATE;
    nb_supprimees INT;
BEGIN
    date_limite := CURRENT_DATE - INTERVAL '1 year' * p_annees_retention;
    
    -- Supprimer les évaluations anciennes
    DELETE FROM Evaluation 
    WHERE EV_DA < date_limite;
    
    GET DIAGNOSTICS nb_supprimees = ROW_COUNT;
    
    RETURN 'SUCCÈS: ' || nb_supprimees || ' évaluations supprimées (antérieures à ' || date_limite || ')';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERREUR: ' || SQLERRM;
END;
$$;
 P   DROP FUNCTION public.sp_nettoyer_donnees_obsoletes(p_annees_retention integer);
       public               postgres    false            �            1255    33065    sp_optimiser_base_donnees()    FUNCTION     �  CREATE FUNCTION public.sp_optimiser_base_donnees() RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Analyse des statistiques des tables
    ANALYZE Utilisateur;
    ANALYZE Cours;
    ANALYZE Enseignement;
    ANALYZE Evaluation;
    
    -- Nettoyage des connexions inactives (si nécessaire)
    -- VACUUM ANALYZE;
    
    RETURN 'SUCCÈS: Base de données optimisée';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERREUR: ' || SQLERRM;
END;
$$;
 2   DROP FUNCTION public.sp_optimiser_base_donnees();
       public               postgres    false            �            1255    33056 (   sp_rapport_enseignant(character varying)    FUNCTION     K  CREATE FUNCTION public.sp_rapport_enseignant(p_nom_enseignant character varying) RETURNS TABLE(evaluation_id character varying, date_evaluation date, cours character varying, pedagogie character varying, accompagnement character varying, interaction character varying, attention character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.EV_ID,
        e.EV_DA,
        e.EV_PEN,
        e.EV_PED,
        e.EV_ACCO,
        e.EV_INCO,
        e.EV_ATTE
    FROM Evaluation e
    WHERE e.EV_CLEX = p_nom_enseignant
    ORDER BY e.EV_DA DESC;
END;
$$;
 P   DROP FUNCTION public.sp_rapport_enseignant(p_nom_enseignant character varying);
       public               postgres    false            �            1255    33066    sp_rapport_sante_base()    FUNCTION     7  CREATE FUNCTION public.sp_rapport_sante_base() RETURNS TABLE(table_name character varying, nombre_enregistrements bigint, taille_estimee text, derniere_modification text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.table_name::VARCHAR(50),
        COALESCE(s.n_tup_ins - s.n_tup_del, 0) as nombre_enregistrements,
        pg_size_pretty(pg_total_relation_size(c.oid))::TEXT as taille_estimee,
        COALESCE(s.last_autoanalyze::TEXT, 'Jamais') as derniere_modification
    FROM information_schema.tables t
    LEFT JOIN pg_stat_user_tables s ON s.relname = t.table_name
    LEFT JOIN pg_class c ON c.relname = t.table_name
    WHERE t.table_schema = 'public'
    AND t.table_name IN ('utilisateur', 'cours', 'enseignement', 'evaluation')
    ORDER BY nombre_enregistrements DESC;
END;
$$;
 .   DROP FUNCTION public.sp_rapport_sante_base();
       public               postgres    false                       1255    33063 x   sp_recherche_evaluations_avancee(character varying, character varying, date, date, character varying, character varying)    FUNCTION     �  CREATE FUNCTION public.sp_recherche_evaluations_avancee(p_enseignant character varying DEFAULT NULL::character varying, p_cours character varying DEFAULT NULL::character varying, p_date_debut date DEFAULT NULL::date, p_date_fin date DEFAULT NULL::date, p_pedagogie character varying DEFAULT NULL::character varying, p_accompagnement character varying DEFAULT NULL::character varying) RETURNS TABLE(ev_id character varying, ev_da date, ev_clex character varying, ev_pen character varying, ev_ped character varying, ev_acco character varying, score_global integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.EV_ID,
        e.EV_DA,
        e.EV_CLEX,
        e.EV_PEN,
        e.EV_PED,
        e.EV_ACCO,
        (CASE 
            WHEN e.EV_PED = 'Excellent' AND e.EV_ACCO = 'Excellent' THEN 100
            WHEN e.EV_PED = 'Très Bien' AND e.EV_ACCO = 'Très Bien' THEN 80
            WHEN e.EV_PED = 'Bien' AND e.EV_ACCO = 'Bien' THEN 60
            ELSE 40
        END) as score_global
    FROM Evaluation e
    WHERE (p_enseignant IS NULL OR UPPER(e.EV_CLEX) LIKE UPPER('%' || p_enseignant || '%'))
    AND (p_cours IS NULL OR UPPER(e.EV_PEN) LIKE UPPER('%' || p_cours || '%'))
    AND (p_date_debut IS NULL OR e.EV_DA >= p_date_debut)
    AND (p_date_fin IS NULL OR e.EV_DA <= p_date_fin)
    AND (p_pedagogie IS NULL OR e.EV_PED = p_pedagogie)
    AND (p_accompagnement IS NULL OR e.EV_ACCO = p_accompagnement)
    ORDER BY score_global DESC, e.EV_DA DESC;
END;
$$;
 �   DROP FUNCTION public.sp_recherche_evaluations_avancee(p_enseignant character varying, p_cours character varying, p_date_debut date, p_date_fin date, p_pedagogie character varying, p_accompagnement character varying);
       public               postgres    false                       1255    33062 '   sp_recherche_globale(character varying)    FUNCTION     �  CREATE FUNCTION public.sp_recherche_globale(p_terme character varying) RETURNS TABLE(table_source character varying, id_element character varying, description text, score_pertinence integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    -- Recherche dans les utilisateurs
    SELECT 
        'Utilisateur'::VARCHAR(20) as table_source,
        u.UT_ID as id_element,
        ('Nom: ' || COALESCE(u.UT_NP, '') || ' - Email: ' || COALESCE(u.UT_MA, ''))::TEXT as description,
        (CASE 
            WHEN UPPER(u.UT_NP) LIKE UPPER('%' || p_terme || '%') THEN 100
            WHEN UPPER(u.UT_MA) LIKE UPPER('%' || p_terme || '%') THEN 90
            WHEN UPPER(u.UT_FO) LIKE UPPER('%' || p_terme || '%') THEN 80
            ELSE 50
        END) as score_pertinence
    FROM Utilisateur u
    WHERE UPPER(u.UT_NP) LIKE UPPER('%' || p_terme || '%')
    OR UPPER(u.UT_MA) LIKE UPPER('%' || p_terme || '%')
    OR UPPER(u.UT_FO) LIKE UPPER('%' || p_terme || '%')
    
    UNION ALL
    
    -- Recherche dans les cours
    SELECT 
        'Cours'::VARCHAR(20) as table_source,
        c.CO_CO as id_element,
        ('Titre: ' || COALESCE(c.CO_TI, ''))::TEXT as description,
        (CASE 
            WHEN UPPER(c.CO_TI) LIKE UPPER('%' || p_terme || '%') THEN 100
            WHEN UPPER(c.CO_CO) LIKE UPPER('%' || p_terme || '%') THEN 90
            ELSE 50
        END) as score_pertinence
    FROM Cours c
    WHERE UPPER(c.CO_TI) LIKE UPPER('%' || p_terme || '%')
    OR UPPER(c.CO_CO) LIKE UPPER('%' || p_terme || '%')
    
    UNION ALL
    
    -- Recherche dans les évaluations
    SELECT 
        'Evaluation'::VARCHAR(20) as table_source,
        e.EV_ID as id_element,
        ('Enseignant: ' || COALESCE(e.EV_CLEX, '') || ' - Date: ' || COALESCE(e.EV_DA::TEXT, ''))::TEXT as description,
        (CASE 
            WHEN UPPER(e.EV_CLEX) LIKE UPPER('%' || p_terme || '%') THEN 100
            WHEN UPPER(e.EV_PEN) LIKE UPPER('%' || p_terme || '%') THEN 90
            ELSE 50
        END) as score_pertinence
    FROM Evaluation e
    WHERE UPPER(e.EV_CLEX) LIKE UPPER('%' || p_terme || '%')
    OR UPPER(e.EV_PEN) LIKE UPPER('%' || p_terme || '%')
    
    ORDER BY score_pertinence DESC, table_source;
END;
$$;
 F   DROP FUNCTION public.sp_recherche_globale(p_terme character varying);
       public               postgres    false            �            1255    33042 f   sp_rechercher_utilisateurs(character varying, character varying, character varying, character varying)    FUNCTION     �  CREATE FUNCTION public.sp_rechercher_utilisateurs(p_sexe character varying DEFAULT NULL::character varying, p_specialite character varying DEFAULT NULL::character varying, p_groupe character varying DEFAULT NULL::character varying, p_filiere character varying DEFAULT NULL::character varying) RETURNS TABLE(ut_id character varying, ut_np character varying, ut_sx character varying, ut_ac character varying, ut_st character varying, ut_sp character varying, ut_gr character varying, ut_fi character varying, ut_ma character varying, ut_fo character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT u.UT_ID, u.UT_NP, u.UT_SX, u.UT_AC, u.UT_ST, u.UT_SP, u.UT_GR, u.UT_FI, u.UT_MA, u.UT_FO
    FROM Utilisateur u
    WHERE (p_sexe IS NULL OR u.UT_SX = p_sexe)
      AND (p_specialite IS NULL OR u.UT_SP = p_specialite)
      AND (p_groupe IS NULL OR u.UT_GR = p_groupe)
      AND (p_filiere IS NULL OR u.UT_FI = p_filiere);
END;
$$;
 �   DROP FUNCTION public.sp_rechercher_utilisateurs(p_sexe character varying, p_specialite character varying, p_groupe character varying, p_filiere character varying);
       public               postgres    false                       1255    33064 *   sp_sauvegarder_statistiques_quotidiennes()    FUNCTION     �  CREATE FUNCTION public.sp_sauvegarder_statistiques_quotidiennes() RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
    nb_users INT;
    nb_cours INT;
    nb_evaluations INT;
    nb_enseignements INT;
BEGIN
    -- Compter les éléments
    SELECT COUNT(*) INTO nb_users FROM Utilisateur;
    SELECT COUNT(*) INTO nb_cours FROM Cours;
    SELECT COUNT(*) INTO nb_evaluations FROM Evaluation;
    SELECT COUNT(*) INTO nb_enseignements FROM Enseignement;
    
    -- Log des statistiques (vous pouvez créer une table de logs)
    -- INSERT INTO logs_statistiques (date_log, nb_users, nb_cours, nb_evaluations, nb_enseignements)
    -- VALUES (CURRENT_DATE, nb_users, nb_cours, nb_evaluations, nb_enseignements);
    
    RETURN 'SUCCÈS: Statistiques sauvegardées - Users: ' || nb_users || 
           ', Cours: ' || nb_cours || ', Évaluations: ' || nb_evaluations || 
           ', Enseignements: ' || nb_enseignements;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERREUR: ' || SQLERRM;
END;
$$;
 A   DROP FUNCTION public.sp_sauvegarder_statistiques_quotidiennes();
       public               postgres    false            �            1255    33055    sp_statistiques_evaluations()    FUNCTION     t  CREATE FUNCTION public.sp_statistiques_evaluations() RETURNS TABLE(total_evaluations bigint, evaluations_ce_mois bigint, nombre_enseignants_evalues bigint, nombre_cours_evalues bigint)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM Evaluation) as total_evaluations,
        (SELECT COUNT(*) FROM Evaluation WHERE DATE_TRUNC('month', EV_DA) = DATE_TRUNC('month', CURRENT_DATE)) as evaluations_ce_mois,
        (SELECT COUNT(DISTINCT EV_CLEX) FROM Evaluation) as nombre_enseignants_evalues,
        (SELECT COUNT(DISTINCT EV_PEN) FROM Evaluation) as nombre_cours_evalues;
END;
$$;
 4   DROP FUNCTION public.sp_statistiques_evaluations();
       public               postgres    false            �            1255    33045 %   sp_supprimer_cours(character varying) 	   PROCEDURE     8  CREATE PROCEDURE public.sp_supprimer_cours(IN p_co_co character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si le cours existe
    IF NOT EXISTS (SELECT 1 FROM Cours WHERE CO_CO = p_co_co) THEN
        p_resultat := 'ERREUR: Cours introuvable';
        RETURN;
    END IF;
    
    -- Supprimer le cours
    DELETE FROM Cours WHERE CO_CO = p_co_co;
    
    p_resultat := 'SUCCÈS: Cours supprimé avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 ]   DROP PROCEDURE public.sp_supprimer_cours(IN p_co_co character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33049 ,   sp_supprimer_enseignement(character varying) 	   PROCEDURE     g  CREATE PROCEDURE public.sp_supprimer_enseignement(IN p_en_co character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'enseignement existe
    IF NOT EXISTS (SELECT 1 FROM Enseignement WHERE EN_CO = p_en_co) THEN
        p_resultat := 'ERREUR: Enseignement introuvable';
        RETURN;
    END IF;
    
    -- Supprimer l'enseignement
    DELETE FROM Enseignement WHERE EN_CO = p_en_co;
    
    p_resultat := 'SUCCÈS: Enseignement supprimé avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 d   DROP PROCEDURE public.sp_supprimer_enseignement(IN p_en_co character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33053 *   sp_supprimer_evaluation(character varying) 	   PROCEDURE     ^  CREATE PROCEDURE public.sp_supprimer_evaluation(IN p_ev_id character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'évaluation existe
    IF NOT EXISTS (SELECT 1 FROM Evaluation WHERE EV_ID = p_ev_id) THEN
        p_resultat := 'ERREUR: Évaluation introuvable';
        RETURN;
    END IF;
    
    -- Supprimer l'évaluation
    DELETE FROM Evaluation WHERE EV_ID = p_ev_id;
    
    p_resultat := 'SUCCÈS: Évaluation supprimée avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 b   DROP PROCEDURE public.sp_supprimer_evaluation(IN p_ev_id character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33041 +   sp_supprimer_utilisateur(character varying) 	   PROCEDURE     `  CREATE PROCEDURE public.sp_supprimer_utilisateur(IN p_ut_id character varying, OUT p_resultat text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Vérifier si l'utilisateur existe
    IF NOT EXISTS (SELECT 1 FROM Utilisateur WHERE UT_ID = p_ut_id) THEN
        p_resultat := 'ERREUR: Utilisateur introuvable';
        RETURN;
    END IF;
    
    -- Supprimer l'utilisateur
    DELETE FROM Utilisateur WHERE UT_ID = p_ut_id;
    
    p_resultat := 'SUCCÈS: Utilisateur supprimé avec succès';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_resultat := 'ERREUR: ' || SQLERRM;
END;
$$;
 c   DROP PROCEDURE public.sp_supprimer_utilisateur(IN p_ut_id character varying, OUT p_resultat text);
       public               postgres    false            �            1255    33058    sp_top_enseignants(integer)    FUNCTION       CREATE FUNCTION public.sp_top_enseignants(p_limite integer DEFAULT 10) RETURNS TABLE(nom_enseignant character varying, nombre_evaluations bigint, score_moyen numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    WITH evaluations_scores AS (
        SELECT 
            EV_CLEX,
            CASE 
                WHEN EV_PED = 'Excellent' THEN 5
                WHEN EV_PED = 'Très Bien' THEN 4
                WHEN EV_PED = 'Bien' THEN 3
                WHEN EV_PED = 'Passable' THEN 2
                ELSE 1
            END as score_pedagogie,
            CASE 
                WHEN EV_ACCO = 'Excellent' THEN 5
                WHEN EV_ACCO = 'Très Bien' THEN 4
                WHEN EV_ACCO = 'Bien' THEN 3
                WHEN EV_ACCO = 'Passable' THEN 2
                ELSE 1
            END as score_accompagnement
        FROM Evaluation
        WHERE EV_CLEX IS NOT NULL
    )
    SELECT 
        es.EV_CLEX as nom_enseignant,
        COUNT(*)::BIGINT as nombre_evaluations,
        AVG((es.score_pedagogie + es.score_accompagnement) / 2.0)::NUMERIC(5,2) as score_moyen
    FROM evaluations_scores es
    GROUP BY es.EV_CLEX
    HAVING COUNT(*) >= 3  -- Au moins 3 évaluations
    ORDER BY score_moyen DESC, nombre_evaluations DESC
    LIMIT p_limite;
END;
$$;
 ;   DROP FUNCTION public.sp_top_enseignants(p_limite integer);
       public               postgres    false            �            1255    33059     sp_valider_donnees_utilisateur()    FUNCTION     �  CREATE FUNCTION public.sp_valider_donnees_utilisateur() RETURNS TABLE(ut_id character varying, probleme text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    -- Vérifier les emails invalides
    SELECT u.UT_ID, 'Email invalide' as probleme
    FROM Utilisateur u
    WHERE u.UT_MA IS NOT NULL 
    AND u.UT_MA NOT LIKE '%@%.%'
    
    UNION ALL
    
    -- Vérifier les sexes invalides
    SELECT u.UT_ID, 'Sexe invalide (doit être M ou F)' as probleme
    FROM Utilisateur u
    WHERE u.UT_SX NOT IN ('M', 'F')
    
    UNION ALL
    
    -- Vérifier les statuts invalides
    SELECT u.UT_ID, 'Statut invalide' as probleme
    FROM Utilisateur u
    WHERE u.UT_ST NOT IN ('A', 'I', 'S') -- Actif, Inactif, Suspendu
    
    ORDER BY ut_id;
END;
$$;
 7   DROP FUNCTION public.sp_valider_donnees_utilisateur();
       public               postgres    false                        1255    33060 #   sp_verifier_integrite_evaluations()    FUNCTION     Q  CREATE FUNCTION public.sp_verifier_integrite_evaluations() RETURNS TABLE(ev_id character varying, probleme text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    -- Vérifier les dates futures
    SELECT e.EV_ID, 'Date d''évaluation dans le futur' as probleme
    FROM Evaluation e
    WHERE e.EV_DA > CURRENT_DATE
    
    UNION ALL
    
    -- Vérifier les champs obligatoires manquants
    SELECT e.EV_ID, 'Champ obligatoire manquant' as probleme
    FROM Evaluation e
    WHERE e.EV_CLEX IS NULL 
    OR e.EV_PEN IS NULL
    OR e.EV_DA IS NULL
    
    ORDER BY ev_id;
END;
$$;
 :   DROP FUNCTION public.sp_verifier_integrite_evaluations();
       public               postgres    false            �            1259    33024    cours    TABLE     �   CREATE TABLE public.cours (
    co_co character varying(12) NOT NULL,
    co_ti character varying(100),
    co_ty character varying(1)
);
    DROP TABLE public.cours;
       public         heap r       postgres    false            �            1259    33029    enseignement    TABLE     �   CREATE TABLE public.enseignement (
    en_co character varying(20) NOT NULL,
    en_ac numeric(10,0),
    en_sm character varying(10),
    en_cc character varying(20),
    en_cr character varying(60)
);
     DROP TABLE public.enseignement;
       public         heap r       postgres    false            �            1259    33034 
   evaluation    TABLE     p  CREATE TABLE public.evaluation (
    ev_id character varying(20) NOT NULL,
    ev_da date,
    ev_clex character varying(60),
    ev_pen character varying(10),
    ev_ped character varying(30),
    ev_acco character varying(10),
    ev_inco character varying(30),
    ev_atte character varying(10),
    ev_getco character varying(10),
    ev_encpa character varying(30),
    ev_usoup character varying(30),
    ev_intre character varying(30),
    ev_intco character varying(30),
    ev_clobp character varying(20),
    ev_utcoc character varying(30),
    ev_oble character varying(30),
    ev_coeve character varying(30)
);
    DROP TABLE public.evaluation;
       public         heap r       postgres    false            �            1259    33019    utilisateur    TABLE     r  CREATE TABLE public.utilisateur (
    ut_id character varying(20) NOT NULL,
    ut_np character varying(50),
    ut_sx character varying(1),
    ut_ac character varying(10),
    ut_st character varying(1),
    ut_sp character varying(2),
    ut_gr character varying(3),
    ut_fi character varying(8),
    ut_ma character varying(20),
    ut_fo character varying(30)
);
    DROP TABLE public.utilisateur;
       public         heap r       postgres    false            ,           2606    33028    cours cours_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.cours
    ADD CONSTRAINT cours_pkey PRIMARY KEY (co_co);
 :   ALTER TABLE ONLY public.cours DROP CONSTRAINT cours_pkey;
       public                 postgres    false    218            .           2606    33033    enseignement enseignement_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.enseignement
    ADD CONSTRAINT enseignement_pkey PRIMARY KEY (en_co);
 H   ALTER TABLE ONLY public.enseignement DROP CONSTRAINT enseignement_pkey;
       public                 postgres    false    219            0           2606    33038    evaluation evaluation_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.evaluation
    ADD CONSTRAINT evaluation_pkey PRIMARY KEY (ev_id);
 D   ALTER TABLE ONLY public.evaluation DROP CONSTRAINT evaluation_pkey;
       public                 postgres    false    220            *           2606    33023    utilisateur utilisateur_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_pkey PRIMARY KEY (ut_id);
 F   ALTER TABLE ONLY public.utilisateur DROP CONSTRAINT utilisateur_pkey;
       public                 postgres    false    217           