USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_InvoiceKey]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_InvoiceKey](
	[InvoiceKey] [int] IDENTITY(2000,1) NOT NULL,
	[InvoiceDate] [datetime] NOT NULL
) ON [PRIMARY]
GO
